
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerRead

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
) -> Customer:
    customer = Customer(**payload.model_dump())

    db.add(customer)

    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Customer data violates a database constraint.",
        ) from exc

    return customer


@router.get("", response_model=list[CustomerRead])
def list_customers(
    db: Session = Depends(get_db),
) -> list[Customer]:
    statement = select(Customer).order_by(Customer.created_at.desc())
    return list(db.scalars(statement).all())
