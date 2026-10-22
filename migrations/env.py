
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.db import Base, get_database_url
from app import models  # noqa: F401

# Alembic configuration.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Models registered on Base will be visible to Alembic.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Configure migrations without opening a database connection."""
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using the configured database connection."""
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
