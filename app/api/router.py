from typing import Any

from fastapi import APIRouter

from app.firestore.endpoints import firestore_user as firestore_user
from app.sqlmodel.api.endpoints import user as sql_user
from app.sqlmodel.api.endpoints import todo as sql_todo
from app.sqlmodel.api.endpoints import thread as thread

api_router = APIRouter()

api_router.include_router(thread.router, prefix="/threads", tags=["Threads"])
api_router.include_router(
    firestore_user.router, prefix="/firestore_users", tags=["Firestore User"]
)
api_router.include_router(sql_user.router, prefix="/sql_users", tags=["SQL User"])
api_router.include_router(sql_todo.router, prefix="/sql_todos", tags=["SQL Todo"])


@api_router.get("/health", tags=["Health"])
def get_health() -> Any:
    return {"status": "OK"}
