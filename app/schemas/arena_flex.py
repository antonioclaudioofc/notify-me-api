from pydantic import BaseModel, EmailStr


class UserCreatedPayload(BaseModel):
    event: str = "user.created"
    email: EmailStr
    name: str


class OwnerPromotedPayload(BaseModel):
    event: str = "owner.promoted"
    email: EmailStr
    name: str
    arena_name: str


class ReservationPayload(BaseModel):
    event: str
    email: EmailStr
    name: str
    owner_email: EmailStr
    owner_name: str
    arena_name: str
    date: str
    time: str


class ReservationReminderPayload(BaseModel):
    event: str = "reservation.reminder"
    email: EmailStr
    arena_name: str
    date: str
    time: str


class ArenaFlexEventRequest(BaseModel):
    event: str
    payload: dict
