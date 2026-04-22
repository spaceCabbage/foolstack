import logging
import threading
import uuid
from django.tasks import task, TaskResult
from django.tasks.backends.base import BaseTaskBackend
from django.core.mail import EmailMessage
from core.email import SmartEmailBackend

logger = logging.getLogger("django.tasks")

class ThreadedTaskBackend(BaseTaskBackend):
    """
    Custom Django 6.0 Task Backend that runs tasks in background threads.
    Provides non-blocking execution without requiring an external worker.
    """
    def enqueue(self, task, args, kwargs):
        from django.utils import timezone
        
        # Create a TaskResult with all required fields for Django 6.0
        result = TaskResult(
            task=task,
            id=str(uuid.uuid4()),
            status=TaskResult.Status.ENQUEUED,  # type: ignore
            backend=self.alias,
            enqueued_at=timezone.now(),
            started_at=None,
            finished_at=None,
            last_attempted_at=None,
            args=args,
            kwargs=kwargs,
            errors=[],
            worker_ids=[],
        )

        def run_in_thread():
            try:
                task.func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Task {task.name} failed: {str(e)}", exc_info=True)

        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()

        return result

@task()
def send_email_task(messages_data: list[dict]):
    """
    Background task to send a batch of emails.
    Uses SmartEmailBackend to perform actual delivery.
    """
    messages = []
    for data in messages_data:
        msg = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=data["from_email"],
            to=data["to"],
        )
        msg.content_subtype = data.get("content_subtype", "plain")
        messages.append(msg)

    # Use SmartEmailBackend to avoid infinite loops with AsyncDispatcherEmailBackend
    backend = SmartEmailBackend()
    try:
        count = backend.send_messages(messages)
        logger.info(f"Successfully sent {count} email(s) via background task.")
        return count
    except Exception as e:
        logger.error(f"Failed to send emails in task: {str(e)}")
        raise
