import asyncio
import os

import pytest
from starlette.testclient import TestClient

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-jwt-secret-key-minimum-thirty-two-characters",
)
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://amp:amp@localhost:5432/amp_test")
os.environ.setdefault("BOOTSTRAP_ADMIN_EMAIL", "test-admin@example.com")
os.environ.setdefault("BOOTSTRAP_ADMIN_PASSWORD", "TestAdmin123!")
os.environ.setdefault("AGENTS_ENABLED", "false")
os.environ["SKIP_APP_LIFESPAN"] = "1"

from app.config import get_settings
from app.main import app, run_migrations
from app.services.bootstrap import bootstrap_admin
from app.db.session import SessionLocal, engine

get_settings.cache_clear()

_bootstrap_done = False


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    global _bootstrap_done
    run_migrations()
    if not _bootstrap_done:

        async def _boot():
            async with SessionLocal() as s:
                await bootstrap_admin(s)

        asyncio.run(_boot())
        _bootstrap_done = True
    yield


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client: TestClient):
    res = client.post(
        "/v1/auth/login",
        json={"email": "test-admin@example.com", "password": "TestAdmin123!"},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
