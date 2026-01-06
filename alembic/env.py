import os
import sys
import socket
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

db_host = os.getenv("POSTGRES_HOST", "db")
db_port = os.getenv("POSTGRES_PORT", "5432")

try:
    socket.gethostbyname(db_host)
except socket.gaierror:
    db_host = "127.0.0.1"
    db_port = "5433"

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if not POSTGRES_USER or not POSTGRES_PASSWORD or not POSTGRES_DB:
    raise RuntimeError("One of the required environment variables is missing!")

database_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{db_host}:{db_port}/{POSTGRES_DB}"

print("SQLALCHEMY_DATABASE_URL:", database_url)

from database import Base
from models import User, Task, Project, Team, TeamMember, TaskComment, TeamInvite, Activity

target_metadata = Base.metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", database_url)

print("Tables:", Base.metadata.tables.keys())

def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=database_url
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
