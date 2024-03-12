import asyncio
from typing import Any

from app.sqlmodel import crud
from fastapi import APIRouter

from app.sqlmodel.api.deps import session_dep

router = APIRouter()


async def sync_func(db) -> None:
    await asyncio.sleep(1)
    return await crud.users.get(db=db, id=1)


async def async_func() -> Any:
    await asyncio.sleep(1)


@router.get("/sync")
async def sync_endpoint(db: session_dep) -> None:
    return await sync_func(db)


@router.get("/async")
async def async_endpoint(db: session_dep) -> None:
    await async_func()
