"""
Custom Django email backend using Resend SDK.

Usage:
    Set EMAIL_BACKEND in settings.py or let it auto-configure:
    - DEBUG mode or LOG_LEVEL=DEBUG: uses console backend
    - No RESEND_API_KEY: uses console backend + logs warning
    - RESEND_API_KEY set: uses this Resend backend
"""

import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from loguru import logger


class ResendEmailBackend(BaseEmailBackend):
    """Django email backend that sends emails via Resend API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        if not settings.RESEND_API_KEY:
            raise ValueError(
                "RESEND_API_KEY is required for ResendEmailBackend. "
                "Set it in your .env file or use console backend for development."
            )
        resend.api_key = settings.RESEND_API_KEY

    def send_messages(self, email_messages):
        """Send one or more EmailMessage objects and return the number sent."""
        if not email_messages:
            return 0

        sent_count = 0
        for message in email_messages:
            try:
                params = {
                    "from": message.from_email,
                    "to": list(message.to),
                    "subject": message.subject,
                    "text": message.body,
                }

                # Handle HTML content (from EmailMultiAlternatives)
                alternatives = getattr(message, "alternatives", None)
                if alternatives:
                    for content, mimetype in alternatives:
                        if mimetype == "text/html":
                            params["html"] = content
                            break

                # Handle CC, BCC, Reply-To
                if message.cc:
                    params["cc"] = list(message.cc)
                if message.bcc:
                    params["bcc"] = list(message.bcc)
                if message.reply_to:
                    params["reply_to"] = message.reply_to[0]

                response = resend.Emails.send(params)  # type: ignore[arg-type]
                logger.debug(f"Email sent via Resend: {response.get('id', 'unknown')}")
                sent_count += 1

            except Exception as e:
                logger.error(f"Failed to send email via Resend: {e}")
                if not self.fail_silently:
                    raise

        return sent_count
