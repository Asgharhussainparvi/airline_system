from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Airline
from app.schemas import AirlineCreate, AirlineRead

router = APIRouter(prefix="/airlines", tags=["Airlines"])


@router.post(
    "",
    response_model=AirlineRead,
    status_code=status.HTTP_201_CREATED,
)
def create_airline(
    payload: AirlineCreate,
    db: Session = Depends(get_db),
) -> Airline:
    airline = Airline(**payload.model_dump())
    db.add(airline)

    try:
        db.commit()
        db.refresh(airline)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Airline code already exists or data violates a database constraint.",
        ) from exc

    return airline


@router.get("", response_model=list[AirlineRead])
def list_airlines(db: Session = Depends(get_db)) -> list[Airline]:
    statement = select(Airline).order_by(Airline.code.asc())
    return list(db.scalars(statement).all())


@router.get("/{airline_id}", response_model=AirlineRead)
def get_airline(
    airline_id: UUID,
    db: Session = Depends(get_db),
) -> Airline:
    airline = db.get(Airline, airline_id)

    if airline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not found.",
        )

    return airline
