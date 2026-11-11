from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from models import Customer 
from dependencies import get_session
from datetime import date, timedelta



router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


class LoginRequest(BaseModel):
    email: str 
    password: str


@router.post("/login")
def login(
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    customer = session.exec(
        select(Customer).where(Customer.email == data.email)
    ).first()

    if not customer:
        raise HTTPException(
            status_code=401,
            detail="E-Mail oder Passwort falsch"
        )

    if customer.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="E-Mail oder Passwort falsch"
        )

    return {
        "message": "Login erfolgreich",
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "email": customer.email
    }