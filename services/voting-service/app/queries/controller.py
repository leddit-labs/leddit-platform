from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db_read import get_read_db


router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)


@router.get(
    "/test",
)
def test():
    return "test"
