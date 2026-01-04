#!/usr/bin/env python3
"""Script to create Alembic configurations for all services."""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Service configurations
SERVICES = {
    "document_service": {
        "type": "sync",
        "database_module": "cds_document.database",
        "models_module": "cds_document.models",
        "config_module": "cds_document.config",
    },
    "product_service": {
        "type": "sync",
        "database_module": "app.repository.db",
        "models_module": "app.repository.product_repo",
        "config_module": "app.config",
    },
    "relationship_service": {
        "type": "sync",
        "database_module": "cds_relationship.db.database",
        "models_module": "cds_relationship.db.models",
        "config_module": "cds_relationship.config",
    },
    "riskprofile_service": {
        "type": "sync",
        "database_module": "app.repository.db",
        "models_module": "app.repository.models",
        "config_module": "app.config",
    },
    "cas_service": {
        "type": "sync",
        "database_module": "cas_audit.database",
        "models_module": "cas_audit.models",
        "config_module": "cas_audit.config",
    },
    "interaction_service": {
        "type": "async",
        "database_module": "cds_interaction.app.database",
        "models_module": "cds_interaction.models",
        "config_module": "cds_interaction.app.config",
    },
    "rmbrain-mainapp": {
        "type": "async",
        "database_module": "app.database",
        "models_module": "app.models",
        "config_module": "app.config",
    },
}

ALEMBIC_INI_TEMPLATE = """# A generic, single database configuration.

[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

SYNC_ENV_PY_TEMPLATE = """\"\"\"Alembic environment configuration for sync database migrations.\"\"\"
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import the Base and models to ensure they're registered
from {database_module} import Base
from {models_module} import *  # noqa: F401, F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def get_url():
    \"\"\"Get database URL from environment or config.\"\"\"
    from {config_module} import settings
    return settings.database_url


def run_migrations_offline() -> None:
    \"\"\"Run migrations in 'offline' mode.\"\"\"
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={{"paramstyle": "named"}},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    \"\"\"Run migrations in 'online' mode.\"\"\"
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

ASYNC_ENV_PY_TEMPLATE = """\"\"\"Alembic environment configuration for async database migrations.\"\"\"
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import the Base and models to ensure they're registered
from {database_module} import Base
from {models_module} import *  # noqa: F401, F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def get_url():
    \"\"\"Get database URL from environment or config.\"\"\"
    from {config_module} import settings
    return settings.database_url


def run_migrations_offline() -> None:
    \"\"\"Run migrations in 'offline' mode.\"\"\"
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={{"paramstyle": "named"}},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    \"\"\"Run migrations with async connection.\"\"\"
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    \"\"\"Run migrations in 'online' mode with async engine.\"\"\"
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    \"\"\"Run migrations in 'online' mode.\"\"\"
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

SCRIPT_Mako_TEMPLATE = """\"\"\"${{message}}

Revision ID: ${{up_revision}}
Revises: ${{down_revision | comma,n}}
Create Date: ${{create_date}}

\"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${{imports if imports else ""}}

# revision identifiers, used by Alembic.
revision: str = ${{repr(up_revision)}}
down_revision: Union[str, None] = ${{repr(down_revision)}}
branch_labels: Union[str, Sequence[str], None] = ${{repr(branch_labels)}}
depends_on: Union[str, Sequence[str], None] = ${{repr(depends_on)}}


def upgrade() -> None:
    ${{upgrades if upgrades else "pass"}}


def downgrade() -> None:
    ${{downgrades if downgrades else "pass"}}
"""


def create_alembic_config(service_name: str, config: dict):
    """Create Alembic configuration files for a service."""
    service_path = REPO_ROOT / service_name
    alembic_path = service_path / "alembic"
    versions_path = alembic_path / "versions"

    # Create directories
    versions_path.mkdir(parents=True, exist_ok=True)
    (versions_path / ".gitkeep").touch()

    # Create alembic.ini
    ini_path = service_path / "alembic.ini"
    if not ini_path.exists():
        ini_path.write_text(ALEMBIC_INI_TEMPLATE)
        print(f"  ✓ Created {ini_path}")

    # Create env.py
    env_py_path = alembic_path / "env.py"
    if config["type"] == "sync":
        env_py_content = SYNC_ENV_PY_TEMPLATE.format(**config)
    else:
        env_py_content = ASYNC_ENV_PY_TEMPLATE.format(**config)
    
    if not env_py_path.exists():
        env_py_path.write_text(env_py_content)
        print(f"  ✓ Created {env_py_path}")

    # Create script.py.mako
    mako_path = alembic_path / "script.py.mako"
    if not mako_path.exists():
        mako_path.write_text(SCRIPT_Mako_TEMPLATE)
        print(f"  ✓ Created {mako_path}")


def main():
    """Create Alembic configurations for all services."""
    print("Creating Alembic configurations...")
    print()

    for service_name, config in SERVICES.items():
        print(f"=== {service_name} ({config['type']}) ===")
        create_alembic_config(service_name, config)
        print()

    print("✓ All Alembic configurations created!")


if __name__ == "__main__":
    main()
