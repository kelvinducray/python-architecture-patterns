from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session

from .config import get_settings

settings = get_settings()

engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DATABASE,
    ),
    echo=True,
    # connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
