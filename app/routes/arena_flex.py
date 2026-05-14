from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_api_key
from app.schemas.arena_flex import (
    UserCreatedPayload,
    OwnerPromotedPayload,
    ReservationPayload,
    ReservationReminderPayload,
)
from app.services.arena_flex.arena_flex_email_service import ArenaFlexEmailService

router = APIRouter(
    prefix="/api/arena-flex",
    tags=["Arena Flex"],
    dependencies=[Depends(verify_api_key)],
)

email_service = ArenaFlexEmailService()


@router.post("/user-created")
def user_created(data: UserCreatedPayload):
    email_service.send_user_created_email(data.model_dump())
    return {"message": "User created notification sent"}


@router.post("/owner-promoted")
def owner_promoted(data: OwnerPromotedPayload):
    email_service.send_owner_promoted_email(data.model_dump())
    return {"message": "Owner promoted notification sent"}


@router.post("/reservation-created")
def reservation_created(data: ReservationPayload):
    if data.event != "reservation.created":
        raise HTTPException(
            status_code=400, detail="Invalid event type for this endpoint"
        )
    email_service.send_reservation_email(data.model_dump(), status="created")
    return {"message": "Reservation created notification sent"}


@router.post("/reservation-confirmed")
def reservation_confirmed(data: ReservationPayload):
    if data.event != "reservation.confirmed":
        raise HTTPException(
            status_code=400, detail="Invalid event type for this endpoint"
        )
    email_service.send_reservation_email(data.model_dump(), status="confirmed")
    return {"message": "Reservation confirmed notification sent"}


@router.post("/reservation-canceled")
def reservation_canceled(data: ReservationPayload):
    if data.event != "reservation.canceled":
        raise HTTPException(
            status_code=400, detail="Invalid event type for this endpoint"
        )
    email_service.send_reservation_email(data.model_dump(), status="canceled")
    return {"message": "Reservation canceled notification sent"}


@router.post("/reservation-reminder")
def reservation_reminder(data: ReservationReminderPayload):
    email_service.send_reservation_reminder_email(data.model_dump())
    return {"message": "Reservation reminder notification sent"}


# Generic events endpoint as requested by the payload examples
@router.post("/events")
def handle_event(data: dict):
    event_type = data.get("event")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing 'event' field in payload")

    try:
        if event_type == "user.created":
            email_service.send_user_created_email(data)
        elif event_type == "owner.promoted":
            email_service.send_owner_promoted_email(data)
        elif event_type in [
            "reservation.created",
            "reservation.confirmed",
            "reservation.canceled",
        ]:
            status = event_type.split(".")[1]
            email_service.send_reservation_email(data, status=status)
        elif event_type == "reservation.reminder":
            email_service.send_reservation_reminder_email(data)
        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported event type: {event_type}"
            )

        return {"message": f"Notification for {event_type} processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
