import datetime
import pytz
from app.core.config import settings
from app.core.smtp import send_email
from app.services.arena_manager.email_service import EmailService
from app.services.template_service import template_service


class ArenaManagerEmailService(EmailService):
    def _get_formatted_now(self):
        utc_zone = pytz.utc
        sp_zone = pytz.timezone("America/Sao_Paulo")
        utc_now = datetime.datetime.now(utc_zone)
        created_at = utc_now.astimezone(sp_zone)
        return created_at.strftime("%d/%m/%Y %H:%M")

    def send_verification_email(self, data: dict):
        verify_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={data['token']}"

        html_content = template_service.render(
            "arena_manager/verification.html",
            email=data["email"],
            formatted_date=self._get_formatted_now(),
            verify_url=verify_url,
        )

        send_email(
            to=data["email"],
            subject="Confirme seu email - Arena Manager",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_owner_promotion_email(self, user: dict, arena: dict):
        html_content = template_service.render(
            "arena_manager/owner_promotion.html",
            name=user["name"],
            arena_name=arena["name"],
            formatted_date=self._get_formatted_now(),
        )

        send_email(
            to=user["email"],
            subject="Parabéns! Você agora é dono de uma arena",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_new_court_email(self, user: dict, arena: dict, court: dict):
        html_content = template_service.render(
            "arena_manager/new_court.html",
            name=user["name"],
            arena_name=arena["name"],
            court_name=court["name"],
            formatted_date=self._get_formatted_now(),
        )

        send_email(
            to=user["email"],
            subject=f"Nova quadra adicionada na arena {arena['name']}",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_reservation_created_email(self, data: dict):
        print(
            f"Reservation created email not yet implemented. Data: {data}", flush=True
        )

    def send_reservation_cancelled_email(self, data: dict):
        print(
            f"Reservation cancelled email not yet implemented. Data: {data}", flush=True
        )
