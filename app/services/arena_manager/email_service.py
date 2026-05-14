from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_verification_email(self, data: dict):
        pass

    @abstractmethod
    def send_owner_promotion_email(self, user: dict, arena: dict):
        pass

    @abstractmethod
    def send_new_court_email(self, user: dict, arena: dict, court: dict):
        pass

    @abstractmethod
    def send_reservation_created_email(self, data: dict):
        pass

    @abstractmethod
    def send_reservation_cancelled_email(self, data: dict):
        pass
