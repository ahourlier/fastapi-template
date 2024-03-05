from faker import Faker
from app.sqlmodel.models.user import UserCreate, UserRead
from sqlmodel import Session
from app.sqlmodel import crud

fake = Faker()


def get_random_user() -> UserCreate:
    user_in = UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
    )
    return user_in


def create_random_user(db: Session) -> UserRead:
    user_in = get_random_user()
    user = crud.users.create(db=db, obj_in=user_in)
    return UserRead.model_validate(user)
