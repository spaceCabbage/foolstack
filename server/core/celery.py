import os

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs):
    """Configure Celery to use our loguru logging setup.

    This signal fires before Celery configures its own logging,
    allowing us to set up loguru instead.
    """
    from core.logging import setup_logging as setup_loguru

    setup_loguru()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery connection."""
    from loguru import logger

    logger.info(f"Debug task executed. Request: {self.request!r}")
