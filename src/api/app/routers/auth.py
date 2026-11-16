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


class UserRegisterRequest(BaseModel):
    email: str
    password: str
    customer_name: str


class LoginRequest(BaseModel):
    email: str 
    password: str

#TODO: Responsemodell verwenden, da passwort noch mit übergeben wird, überprüfen, dass email richtig übergeben wird. 
@router.post("/register")
def create_user_via_register(
    data: UserRegisterRequest,
    session: Session = Depends(get_session)
) -> Customer:
    
    customer = session.exec(
        select(Customer).where(Customer.email == data.email)
    ).first()

    if customer:
        raise HTTPException(
        status_code=400,
        detail="E-Mail ist bereits registriert"
        )

    db_customer = Customer.model_validate(data)
    session.add(db_customer)    
    session.commit()
    session.refresh(db_customer)
    return db_customer

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