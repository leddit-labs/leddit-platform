from fastapi import APIRouter, Depends
from neo4j import Driver

from .database import get_db
from .repository import CommentRepository
from .schemas import CommentCreate, CommentResponse, CommentUpdate
from .service import CommentService

router = APIRouter(prefix="/api/v1", tags=["comments"])


def get_comment_service(db: Driver = Depends(get_db)) -> CommentService:
    repository = CommentRepository(db)
    return CommentService(repository)


@router.post("/comments", response_model=CommentResponse, status_code=201)
def create_comment(payload: CommentCreate, service: CommentService = Depends(get_comment_service)):
    return service.create_comment(payload)


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, service: CommentService = Depends(get_comment_service)):
    return service.get_comment(comment_id)


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def list_comments(post_id: str, service: CommentService = Depends(get_comment_service)):
    return service.list_comments_for_post(post_id)


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
):
    return service.update_comment(comment_id, payload)


@router.delete("/comments/{comment_id}", response_model=CommentResponse)
def delete_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
):
    return service.delete_comment(comment_id)
