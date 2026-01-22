import sys
import pathlib
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.config.config import load_config
from app.db.models import Base  # noqa

# Alembic Config object
config = context.config

# Используем sync URL для Alembic
cfg = load_config()
config.set_main_option("sqlalchemy.url", cfg.postgres.sync_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata
target_metadata = Base.metadata

# Offline
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Online
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
