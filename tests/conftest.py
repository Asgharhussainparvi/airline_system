from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from app.db import engine, get_db
from app.main import app


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()

    TestSessionLocal = sessionmaker(
        bind=connection,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
