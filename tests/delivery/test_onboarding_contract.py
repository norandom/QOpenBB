"""Real GET route and SQLite questionnaire contract, without service startup."""
import os
from pathlib import Path
import subprocess
import unittest


def test_onboarding_contract():
    import pytest

    python = os.environ.get("QOPENBB_STARTUP_PYTHON")
    if not python:
        pytest.skip("Run --probe with the restored backend interpreter or packaged image")
    result = subprocess.run([python, str(Path(__file__).resolve()), "--probe"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


class OnboardingContract(unittest.IsolatedAsyncioTestCase):
    __test__ = False

    async def asyncSetUp(self):
        from tempfile import TemporaryDirectory
        from types import SimpleNamespace
        from uuid import uuid4
        from fastapi import FastAPI, HTTPException
        from httpx import ASGITransport, AsyncClient
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
        from api.models import DeveloperOnboarding
        from routers.pro.index import router

        self.temp = TemporaryDirectory()
        self.engine = create_async_engine(f"sqlite+aiosqlite:///{self.temp.name}/test.db")
        self.user = SimpleNamespace(uuid=uuid4())
        async with self.engine.begin() as connection:
            await connection.exec_driver_sql("CREATE TABLE user (uuid CHAR(32) PRIMARY KEY)")
            await connection.exec_driver_sql("INSERT INTO user VALUES (?)", (self.user.uuid.bytes,))
            await connection.run_sync(DeveloperOnboarding.__table__.create)
        self.db = AsyncSession(self.engine, expire_on_commit=False)
        self.app = FastAPI()
        self.route = next(route for route in router.routes
                          if route.path == "/pro/pro-developer-onboarding-info"
                          and "GET" in route.methods)
        self.app.include_router(router)
        self.authenticated = True

        async def authenticate():
            if not self.authenticated:
                raise HTTPException(401, "Authentication required")
            return self.user

        async def database():
            yield self.db

        for dependency in self.route.dependant.dependencies:
            if dependency.name == "user":
                self.app.dependency_overrides[dependency.call] = authenticate
            elif dependency.name == "db":
                self.app.dependency_overrides[dependency.call] = database
            else:
                self.app.dependency_overrides[dependency.call] = lambda: None
        self.client = AsyncClient(transport=ASGITransport(app=self.app, raise_app_exceptions=False),
                                  base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        await self.db.close()
        await self.engine.dispose()
        self.temp.cleanup()

    async def test_absent_questionnaire_is_null_without_writing(self):
        from sqlalchemy import func, select
        from api.models import DeveloperOnboarding

        response = await self.client.get(self.route.path)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())
        self.assertEqual(await self.db.scalar(select(func.count()).select_from(DeveloperOnboarding)), 0)

    async def test_saved_answers_and_skip_are_preserved(self):
        from api.models import DeveloperOnboarding

        answers = dict(primary_usage="professional", organization="Research", role="Analyst",
                       programming_experience="intermediate-advanced", data_types=["equity"],
                       other_data_types="fundamentals", organization_name="Example", skip_onboarding=True)
        self.db.add(DeveloperOnboarding(user_uuid=self.user.uuid, **answers))
        await self.db.commit()
        response = await self.client.get(self.route.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), dict(primaryUsage="professional", organization="Research",
                         role="Analyst", programmingExperience="intermediate-advanced", dataTypes=["equity"],
                         otherDataType="fundamentals", organizationName="Example", skipOnboarding=True))

    async def test_authentication_failure_is_not_empty_questionnaire(self):
        self.authenticated = False
        response = await self.client.get(self.route.path)
        self.assertEqual(response.status_code, 401)

    async def test_database_failure_remains_visible(self):
        from unittest.mock import AsyncMock, patch

        with patch.object(self.db, "execute", AsyncMock(side_effect=RuntimeError("database unavailable"))):
            response = await self.client.get(self.route.path)
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main(argv=[__file__], verbosity=2)
