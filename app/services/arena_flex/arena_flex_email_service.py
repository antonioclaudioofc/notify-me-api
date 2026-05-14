import datetime
import pytz
from app.core.config import settings
from app.core.smtp import send_email
from app.services.template_service import template_service


class ArenaFlexEmailService:
    def __init__(self):
        self.from_addr = settings.MAIL_FROM_ARENAMANAGER

    def _get_formatted_now(self):
        sp_zone = pytz.timezone("America/Sao_Paulo")
        return (
            datetime.datetime.now(pytz.utc)
            .astimezone(sp_zone)
            .strftime("%d/%m/%Y %H:%M")
        )

    def send_user_created_email(self, data: dict):
        html_content = template_service.render(
            "arena_flex/user_created.html",
            name=data["name"],
            email=data["email"],
            formatted_date=self._get_formatted_now(),
        )
        send_email(
            to=data["email"],
            subject="Bem-vindo ao Arena Flex!",
            html_content=html_content,
            from_addr=self.from_addr,
        )

    def send_owner_promoted_email(self, data: dict):
        html_content = template_service.render(
            "arena_flex/owner_promoted.html",
            name=data["name"],
            arena_name=data["arena_name"],
        )
        send_email(
            to=data["email"],
            subject=f"Parabéns! Você agora é dono da arena {data['arena_name']}",
            html_content=html_content,
            from_addr=self.from_addr,
        )

    def send_reservation_email(self, data: dict, status: str):
        status_colors = {
            "created": "#3b82f6",
            "confirmed": "#10b981",
            "canceled": "#ef4444",
        }
        status_titles = {
            "created": "Reserva Aguardando Confirmação",
            "confirmed": "Sua Reserva foi Confirmada!",
            "canceled": "Sua Reserva foi Cancelada",
        }

        status_labels = {
            "created": "Pendente",
            "confirmed": "Confirmada",
            "canceled": "Cancelada",
        }

        color = status_colors.get(status, "#3b82f6")
        title = status_titles.get(status, "Atualização de Reserva")
        label = status_labels.get(status, "Status Atualizado")


        customer_html = template_service.render(
            "arena_flex/reservation_status.html",
            name=data["name"],
            arena_name=data["arena_name"],
            date=data["date"],
            time=data["time"],
            color=color,
            title=title,
            status_label=label,
            status_type=status,
        )
        send_email(
            to=data["email"],
            subject=f"{title} - {data['arena_name']}",
            html_content=customer_html,
            from_addr=self.from_addr,
        )

        owner_html = template_service.render(
            "arena_flex/reservation_status.html",
            name=data["owner_name"],
            arena_name=data["arena_name"],
            date=data["date"],
            time=data["time"],
            color=color,
            title=title,
            status_label=label,
            status_type=status,
        )

        send_email(
            to=data["owner_email"],
            subject=f"{title} - {data['arena_name']} (Cópia do Proprietário)",
            html_content=owner_html,
            from_addr=self.from_addr,
        )

    def send_reservation_reminder_email(self, data: dict):
        html_content = template_service.render(
            "arena_flex/reservation_reminder.html",
            arena_name=data["arena_name"],
            date=data["date"],
            time=data["time"],
        )
        send_email(
            to=data["email"],
            subject=f"Lembrete: Sua partida em {data['arena_name']} está chegando!",
            html_content=html_content,
            from_addr=self.from_addr,
        )
