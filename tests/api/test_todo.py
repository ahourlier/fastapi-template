from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from tests.utils.todo import create_random_todo, get_random_todo

DATASOURCES_URL = f"{settings.API_PREFIX}/sql_todos"


async def test_create_todo(client: TestClient, db: AsyncSession) -> None:
    todo = get_random_todo()
    response = client.post(
        DATASOURCES_URL,
        json=jsonable_encoder(todo),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("id") is not None


async def test_get_todo(client: TestClient, db: AsyncSession) -> None:
    response = client.get(
        f"{DATASOURCES_URL}/{1}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("id") == 1


async def test_get_todos(client: TestClient, db: AsyncSession) -> None:
    response = client.get(
        f"{DATASOURCES_URL}",
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get("total") == 1
    items = content.get("items")
    assert len(items) == 1
    assert items[0].get("id") == 1


async def test_update_todo(client: TestClient, db: AsyncSession) -> None:
    todo = await create_random_todo(db, commit=True)
    todo.title = "updated"
    response = client.put(
        f"{DATASOURCES_URL}/{todo.id}",
        json=jsonable_encoder(todo),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("title") == todo.title


async def test_delete_todo(client: TestClient, db: AsyncSession) -> None:
    todo = await create_random_todo(db, commit=True)
    response = client.delete(
        f"{DATASOURCES_URL}/{todo.id}",
    )
    assert response.status_code == 200

    response = client.get(
        f"{DATASOURCES_URL}/{todo.id}",
    )
    assert response.status_code == 404
