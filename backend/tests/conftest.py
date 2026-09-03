import os
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set testing environment before importing app
os.environ["APP_ENV"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["STORAGE_BASE_DIR"] = "./storage/test_assets"
os.environ["LLM_PROVIDER"] = "mock"
os.environ["IMAGE_PROVIDER"] = "mock"
os.environ["FLUX_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENROUTER_API_KEY"] = ""
os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""

from app.database import Base, get_db
from app.main import create_app

from sqlalchemy.pool import StaticPool

# In-memory SQLite Engine with StaticPool for Testing
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    future=True
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Sets up temporary test storage directories."""
    test_storage = Path("./storage/test_assets")
    test_storage.mkdir(parents=True, exist_ok=True)
    yield
    # Teardown storage if needed
    import shutil
    if test_storage.exists():
        shutil.rmtree(test_storage, ignore_errors=True)


@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh database schema for each test function."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with injected test database session."""
    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
