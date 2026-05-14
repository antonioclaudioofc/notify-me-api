from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.schemas.email_verification import RequestEmailVerification
from app.schemas.requests import OwnerPromotionRequest, NewCourtRequest
from app.services.arena_manager.arena_manager_email_service import (
    ArenaManagerEmailService,
)

router = APIRouter(
    prefix="/api/arena-manager",
    tags=["Arena Manager"],
    dependencies=[Depends(verify_api_key)],
)

email_service = ArenaManagerEmailService()


@router.post("/verification")
def send_verification_email(data: RequestEmailVerification):
    email_service.send_verification_email(data.model_dump())
    return {"message": "Verification email sent"}


@router.post("/owner-promotion")
def send_owner_promotion_email(data: OwnerPromotionRequest):
    email_service.send_owner_promotion_email(
        data.user.model_dump(), data.arena.model_dump()
    )
    return {"message": "Owner promotion email sent"}


@router.post("/new-court")
def send_new_court_email(data: NewCourtRequest):
    email_service.send_new_court_email(
        data.user.model_dump(),
        data.arena.model_dump(),
        data.court.model_dump(),
    )
    return {"message": "New court email sent"}


@router.post("/reservation-created")
def send_reservation_created_email(data: dict):
    email_service.send_reservation_created_email(data)
    return {"message": "Reservation created email sent"}


@router.post("/reservation-cancelled")
def send_reservation_cancelled_email(data: dict):
    email_service.send_reservation_cancelled_email(data)
    return {"message": "Reservation cancelled email sent"}
