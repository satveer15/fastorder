import pytest
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth.utils import hash_password

# Test database - use file-based in-memory SQLite with shared cache
# This ensures all connections within a test share the same database
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Use StaticPool to ensure single connection is reused
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Get TestClient with test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Mock the scheduler to prevent it from starting during tests
    with patch('app.scheduler.start_scheduler'), patch('app.scheduler.stop_scheduler'):
        yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db):
    """Create a test user"""
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash=hash_password("testpass123")
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user
