from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.sqlmodel.models.user import User
from tests.utils.user import create_random_user, get_random_user


DATASOURCES_URL = f"{settings.API_PREFIX}/sql_users"


async def test_create_user(client: TestClient, db: AsyncSession) -> None:
    user = get_random_user()
    response = client.post(
        DATASOURCES_URL,
        json=jsonable_encoder(user),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("email") == user.email
    # Delete user
    obj = (await db.scalars(select(User).where(User.id == id))).first()
    await db.delete(obj)
    await db.commit()


async def test_get_user(client: TestClient, db: AsyncSession) -> None:
    user = await create_random_user(db)
    response = client.get(
        f"{DATASOURCES_URL}/{user.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("id") is not None

    # Delete user
    obj = await db.scalars(select(User).where(User.id == id)).first()
    await db.delete(obj)
    await db.commit()


@pytest.mark.anyio
async def test_get_users(client: TestClient, db: AsyncSession) -> None:
    # users = [
    #     await create_random_user(db),
    #     await create_random_user(db),
    #     await create_random_user(db),
    # ]
    response = await client.get(
        f"{DATASOURCES_URL}",
    )
    assert response.status_code == 200

    # content = response.json()
    # assert content.get("total") == len(users)
    # items = content.get("items")
    # assert len(items) == len(users)

    # for user in users:
    #     await db.delete(db.exec(select(User).where(User.id == user.id)).first())
    #     await db.commit()
