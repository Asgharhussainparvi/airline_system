import uuid

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Airline, Customer


def test_database_tables_exist() -> None:
    with engine.connect() as connection:
        inspector = inspect(connection)
        tables = set(inspector.get_table_names(schema="public"))

    assert "customers" in tables
    assert "airlines" in tables


def test_customer_and_airline_can_be_inserted(
    db_session: Session,
) -> None:
    customer_id = uuid.uuid4()
    airline_id = uuid.uuid4()

    customer = Customer(
        id=customer_id,
        display_name="Test Customer",
        email=f"{customer_id}@example.test",
    )
    airline = Airline(
        id=airline_id,
        code=f"T{airline_id.hex[:2].upper()}",
        name="Test Airline",
    )

    db_session.add_all([customer, airline])
    db_session.flush()

    assert db_session.get(Customer, customer_id) is not None
    assert db_session.get(Airline, airline_id) is not None
