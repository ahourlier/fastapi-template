import json

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.todo import create_random_todo, get_random_todo

DATASOURCES_URL = f"{settings.API_PREFIX}/sql_todos"


def test_create_todo(client: TestClient, db: Session) -> None:
    todo = get_random_todo()
    response = client.post(
        DATASOURCES_URL,
        json=jsonable_encoder(todo),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("title") == todo.title


def test_get_todo(client: TestClient, db: Session) -> None:
    todo = create_random_todo(db)
    response = client.get(
        f"{DATASOURCES_URL}/{todo.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("title") == todo.title


def test_get_todos(client: TestClient, db: Session) -> None:
    todo = create_random_todo(db)
    response = client.get(
        f"{DATASOURCES_URL}",
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get("total") == 1

    items = content.get("items")
    assert len(items) == 1
    assert items[0].get("title") == todo.title


def test_get_filtered_todos(client: TestClient, db: Session) -> None:
    todo0 = create_random_todo(db)
    todo1 = create_random_todo(db)  # noqa
    todo2 = create_random_todo(db)  # noqa

    query_filters = [
        {"field": "title", "operator": "eq", "value": todo0.title},
        {"field": "priority", "operator": "=", "value": todo0.priority},
    ]
    query_params = {
        "skip": 0,
        "limit": None,
        "sort": None,
        "is_desc": False,
        "filters": json.dumps(query_filters),
    }

    response = client.get(
        DATASOURCES_URL,
        params=query_params,
    )
    print(response.url)
    assert response.status_code == 200

    content = response.json()
    assert content.get("total") == 1

    items = content.get("items")
    assert len(items) == content.get("total")
    assert items[0].get("id") == todo0.id


def test_update_todo(client: TestClient, db: Session) -> None:
    todo = create_random_todo(db)
    todo.title = "updated"
    response = client.put(
        f"{DATASOURCES_URL}/{todo.id}",
        json=jsonable_encoder(todo),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("title") == todo.title


def test_delete_todo(client: TestClient, db: Session) -> None:
    todo = create_random_todo(db)
    response = client.delete(
        f"{DATASOURCES_URL}/{todo.id}",
    )
    assert response.status_code == 200

    response = client.get(
        f"{DATASOURCES_URL}/{todo.id}",
    )
    assert response.status_code == 404
