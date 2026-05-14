import datetime
import pytz
from app.core.config import settings
from app.core.smtp import send_email
from app.schemas.contact import RequestContact
from app.services.antonio_claudio_dev.email_service import EmailService
from app.services.template_service import template_service


class AntonioClaudioDevEmailService(EmailService):
    def send_message_from_payload(self, payload: dict):
        contact = RequestContact.model_validate(payload)
        self.send_message(contact)

    def send_message(self, contact: RequestContact):
        utc_zone = pytz.utc
        sp_zone = pytz.timezone("America/Sao_Paulo")
        utc_now = datetime.datetime.now(utc_zone)
        created_at = utc_now.astimezone(sp_zone)
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        html_content = template_service.render(
            "antonio_claudio_dev/contact.html",
            name=contact.name,
            email=contact.email,
            message=contact.message,
            formatted_date=formatted_date,
        )

        send_email(
            to=settings.MAIL_TO,
            subject=f"Novo contato de {contact.name}",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ANTONIOCLAUDIODEV,
        )
