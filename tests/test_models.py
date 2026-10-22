import uuid

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

from app.db import Base, get_database_url
from app.models import Airline, Customer


def test_database_tables_exist() -> None:
    engine = create_engine(get_database_url())

    try:
        inspector = inspect(engine)
        tables = set(inspector.get_table_names(schema="public"))

        assert "customers" in tables
        assert "airlines" in tables
    finally:
        engine.dispose()


def test_customer_and_airline_can_be_inserted() -> None:
    engine = create_engine(get_database_url())

    customer_id = uuid.uuid4()
    airline_id = uuid.uuid4()

    try:
        with Session(engine) as session:
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

            session.add_all([customer, airline])
            session.commit()

            assert session.get(Customer, customer_id) is not None
            assert session.get(Airline, airline_id) is not None

            session.delete(customer)
            session.delete(airline)
            session.commit()
    finally:
        engine.dispose()