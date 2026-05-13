from fastapi import APIRouter, Depends, HTTPException
from neo4j import Driver

from .database import get_db
from .repository import CommentRepository
from .schemas import CommentCreate, CommentResponse, CommentUpdate
from .service import CommentService

router = APIRouter(prefix="", tags=["comments"])


def get_comment_service(db: Driver = Depends(get_db)) -> CommentService:
    repository = CommentRepository(db)
    return CommentService(repository)


@router.post("/comments", response_model=CommentResponse, status_code=201)
def create_comment(payload: CommentCreate, service: CommentService = Depends(get_comment_service)):
    if payload.parent_id is not None:
        parent = service.get_comment_raw(payload.parent_id)
        if parent is None:
            raise HTTPException(status_code=400, detail="Parent comment does not exist")
        if parent.post_id != payload.post_id:
            raise HTTPException(status_code=400, detail="Parent comment belongs to another post")

    return service.create_comment(payload)


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, service: CommentService = Depends(get_comment_service)):
    comment = service.get_comment_raw(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return service._to_out(comment)


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def list_comments(post_id: str, service: CommentService = Depends(get_comment_service)):
    return service.list_comments_for_post(post_id)


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
):
    comment = service.get_comment_raw(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.deleted_at is not None:
        raise HTTPException(status_code=409, detail="Deleted comments cannot be edited")

    return service.update_comment(comment, payload)


@router.delete("/comments/{comment_id}", response_model=CommentResponse)
def delete_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
):
    comment = service.get_comment_raw(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.deleted_at is not None:
        return service._to_out(comment)

    return service.delete_comment(comment)
