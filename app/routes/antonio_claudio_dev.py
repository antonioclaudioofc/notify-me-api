from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.schemas.contact import RequestContact
from app.services.antonio_claudio_dev.antonio_claudio_dev_email_service import (
    AntonioClaudioDevEmailService,
)

router = APIRouter(
    prefix="/api/antonio-claudio-dev",
    tags=["Antonio Claudio Dev"],
    dependencies=[Depends(verify_api_key)],
)

email_service = AntonioClaudioDevEmailService()


@router.post("/contact")
def send_contact_message(data: RequestContact):
    email_service.send_message(data)
    return {"message": "Contact email sent"}
