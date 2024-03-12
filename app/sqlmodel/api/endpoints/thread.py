import asyncio
from anyio import to_thread
from typing import Any

from app.sqlmodel import crud
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.sqlmodel.api.deps import get_session

to_thread.current_default_thread_limiter().total_tokens = 500

router = APIRouter()


def sync_func(db) -> None:
    return crud.users.get(db=db, id=1)


async def async_func() -> Any:
    await asyncio.sleep(0.5)


@router.get("/sync")
def sync_endpoint(db: Session = Depends(get_session)) -> None:
    sync_func(db)


@router.get("/async")
async def async_endpoint(db: Session = Depends(get_session)) -> None:
    await async_func(db)
