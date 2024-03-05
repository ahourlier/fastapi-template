from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.user import get_random_user, create_random_user


DATASOURCES_URL = f"{settings.API_PREFIX}/sql_users"


def test_create_user(client: TestClient, db: Session) -> None:
    user = get_random_user()
    response = client.post(
        DATASOURCES_URL,
        json=jsonable_encoder(user),
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("email") == user.email


def test_get_user(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    response = client.get(
        f"{DATASOURCES_URL}/{user.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("first_name") == user.first_name


def test_get_users(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    response = client.get(
        f"{DATASOURCES_URL}",
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get("total") == 1

    items = content.get("items")
    assert len(items) == 1
    assert items[0].get("first_name") == user.first_name
