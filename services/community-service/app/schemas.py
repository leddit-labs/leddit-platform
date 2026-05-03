import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Helper functions
SLUG_RE = re.compile(r"^[a-z0-9_]{3,50}$")


def _to_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", value.lower())


# Community
class CommunityCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    slug: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=1000)

    @field_validator("slug", mode="before")
    @classmethod
    def normalise_slug(cls, v: str) -> str:
        return _to_slug(v)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not SLUG_RE.match(v):
            raise ValueError(
                "Slug must be 3–50 characters, lowercase letters, digits, or underscores only."
            )
        return v


class CommunityUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, max_length=1000)


class CommunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    owner_id: uuid.UUID
    is_archived: bool
    member_count: int = 0
    created_at: datetime
    updated_at: datetime


class CommunityListResponse(BaseModel):
    items: list[CommunityResponse]
    total: int
    page: int
    page_size: int


# Membership
class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    community_id: uuid.UUID
    user_id: uuid.UUID
    joined_at: datetime


# Moderators
class ModeratorAssign(BaseModel):
    user_id: uuid.UUID


class ModeratorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    community_id: uuid.UUID
    user_id: uuid.UUID
    granted_by: uuid.UUID
    granted_at: datetime


# Rules
class RuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    position: int = Field(0, ge=0)


class RuleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    position: int | None = Field(None, ge=0)


class RuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    community_id: uuid.UUID
    title: str
    description: str | None
    position: int


# gRPC
class CommunityExistsResponse(BaseModel):
    exists: bool
    is_deleted: bool
    owner_id: uuid.UUID | None


class MembershipCheckResponse(BaseModel):
    is_member: bool
    is_moderator: bool
    is_owner: bool
