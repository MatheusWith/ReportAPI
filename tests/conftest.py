from collections.abc import Callable, Generator
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.app.core.config import settings
from src.app.main import app

DATABASE_URI = settings.DBAPOSTGRES_URI
DATABASE_PREFIX = settings.DBAPOSTGRES_SYNC_PREFIX

sync_engine = create_engine(DATABASE_PREFIX + DATABASE_URI)
local_session = sessionmaker(autoflush=False,bind=sync_engine)

fake = Faker()

@pytest.fixture(scope="session")
def client() -> Generator[TestClient,Any, None]:
    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides = {}
    sync_engine.dispose()

@pytest.fixture
def db() -> Generator[Session,Any,None]:
    session = local_session()
    yield session
    session.close()

def override_dependency(dependency: Callable[..., Any], mocked_response: Any) -> None:
    app.dependency_overrides[dependency] = lambda: mocked_response


@pytest.fixture
def mock_db():
    """Mock database session for unit tests."""
    return Mock(spec=AsyncSession)
