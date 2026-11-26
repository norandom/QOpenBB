"""Seed two ordinary analyst accounts in the disposable packaged Workspace."""

import asyncio
import json
import os
from pathlib import Path
from uuid import UUID

async def provision():
    from sqlalchemy import insert

    from api.base import clean_email
    from api.database import aget_write_db
    from api.models import User

    role = UUID(json.loads(Path("user_create.json").read_text())["permissions_uuid"])
    async for db in aget_write_db():
        for analyst in ("owner", "peer"):
            email = f"story-{analyst}@example.com"
            await db.execute(insert(User).values(
                email=email, clean_email=clean_email(email), first_name="Story", last_name="Analyst",
                permissions_uuid=role, is_superuser=False, confirmed=True, billing_active=True,
                password=os.environ[f"STORY_{analyst.upper()}_PASSWORD"],
            ))
        await db.commit()


if __name__ == "__main__":
    # The image entrypoint exports its bootstrap settings only in its process tree.
    for setting in Path("/data/secrets.env").read_text().splitlines():
        key, value = setting.split("=", 1)
        os.environ[key] = value
    asyncio.run(provision())
