import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.dependency import get_db
from app.config import TEST_DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from app.models.models import User, Event
from app.utils import hash_password

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="session")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(db):
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password = hash_password("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def test_event(db):
    event = Event(
        title="Test Event",
        description="This is a test event.",
        owner_id=test_user.id,
        start_datetime="",
        end_datetime="",
        location_url="",
        max_participant=5,
        is_active=False,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return event