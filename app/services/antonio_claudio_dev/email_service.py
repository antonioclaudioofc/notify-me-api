from abc import ABC, abstractmethod

from app.schemas.contact import RequestContact


class EmailService(ABC):
    @abstractmethod
    def send_message_from_payload(self, payload: dict):
        pass

    @abstractmethod
    def send_message(self, contact: RequestContact):
        pass
