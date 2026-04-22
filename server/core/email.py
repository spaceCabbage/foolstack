import logging
from typing import Any

import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend

logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    """
    Email backend for Resend API.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY

    def send_messages(self, email_messages):
        if not email_messages or not settings.RESEND_API_KEY:
            return 0

        count = 0
        for message in email_messages:
            try:
                # Determine content type (HTML vs Text)
                is_html = message.content_subtype == "html"

                params: dict[str, Any] = {
                    "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
                    "to": message.to,
                    "subject": message.subject,
                }

                if is_html:
                    params["html"] = message.body
                else:
                    params["text"] = message.body

                resend.Emails.send(params)
                count += 1
            except Exception as e:
                logger.error(f"Resend API error: {str(e)}")
                if not self.fail_silently:
                    raise
        return count


class SmartEmailBackend(BaseEmailBackend):
    """
    Unified backend:
    - Dev: Console + Resend (if key exists)
    - Prod: Resend only (if key exists)
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.console = ConsoleBackend()
        self.resend = ResendEmailBackend(fail_silently=fail_silently)

    def send_messages(self, email_messages):
        # 1. Always log to console in development
        if settings.DEBUG:
            self.console.send_messages(email_messages)

        # 2. Send via Resend if key exists
        if settings.RESEND_API_KEY:
            return self.resend.send_messages(email_messages)

        return len(list(email_messages)) if settings.DEBUG else 0


class AsyncDispatcherEmailBackend(BaseEmailBackend):
    """
    Default Django Email Backend that enqueues emails into the
    Django 6.0 task system for asynchronous processing.
    """

    def send_messages(self, email_messages):
        from core.tasks import send_email_task

        serialized_messages = []
        for msg in email_messages:
            serialized_messages.append(
                {
                    "subject": msg.subject,
                    "body": msg.body,
                    "from_email": msg.from_email or settings.DEFAULT_FROM_EMAIL,
                    "to": msg.to,
                    "content_subtype": msg.content_subtype,
                }
            )

        if serialized_messages:
            send_email_task.enqueue(serialized_messages)

        return len(list(email_messages))
