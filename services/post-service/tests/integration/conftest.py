import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from testcontainers.rabbitmq import RabbitMqContainer

SERVICE_ROOT = Path(__file__).resolve().parents[2]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app import db as app_db

# Mock the database to isolate the test to focus on RabbitMQ integration only.
# This keeps the test fast and avoids the need for a Postgres container.
app_db.Base.metadata.create_all = lambda *args, **kwargs: None

from app.config import settings
from app.main import app
from app.post_repository import PostRepository

# Spin up a RabbitMQ container for the test session
@pytest.fixture(scope="session")
def rabbitmq_container() -> RabbitMqContainer:
    with RabbitMqContainer("rabbitmq:3-alpine") as container:
        yield container

# Point the app to the test RabbitMQ instance
@pytest.fixture(scope="session", autouse=True)
def rabbitmq_settings(rabbitmq_container: RabbitMqContainer):
    settings.rabbitmq_host = rabbitmq_container.get_container_host_ip()
    settings.rabbitmq_port = int(rabbitmq_container.get_exposed_port(rabbitmq_container.port))
    yield


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, rabbitmq_settings):
    def fake_create(self, db, data):
        # Return a dummy post object instead of hitting the real DB
        return SimpleNamespace(
            id=1,
            u_id=uuid4(),
            community_id=data.community_id,
            author_id=data.author_id,
            title=data.title,
            content=data.content,
            created_at=datetime.now(timezone.utc),
            deleted_at=None,
        )
    
    # Swap the real create method with our fake one
    monkeypatch.setattr(PostRepository, "create", fake_create)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()