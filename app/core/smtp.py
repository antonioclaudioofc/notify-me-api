import smtplib
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(
    to: str, subject: str, html_content: str, from_addr: str, retries: int = 3
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to

    msg.attach(MIMEText(html_content, "html"))

    _, sender_email = parseaddr(from_addr)

    attempt = 0
    while attempt < retries:
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(sender_email, [to], msg.as_string())

            logger.info(f"Email sent successfully to {to} (Subject: {subject})")
            return True

        except Exception as e:
            attempt += 1
            logger.error(
                f"Attempt {attempt}/{retries} failed to send email to {to}: {str(e)}"
            )
            if attempt < retries:
                time.sleep(2**attempt)
            else:
                logger.critical(f"All attempts failed for email to {to}")
                raise e
