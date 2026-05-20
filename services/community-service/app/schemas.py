from pydantic import BaseModel, Field

# ----------------
# Community
# ----------------
class CommunityCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    description: str = Field(default="", max_length=500)


class CommunityUpdate(BaseModel):
    description: str | None = None


class CommunityOut(BaseModel):
    id: str
    name: str
    description: str
    created_by: str

    class Config:
        from_attributes = True

# ----------------
# Moderator
# ----------------
class ModeratorAdd(BaseModel):
    user_id: str = Field(..., min_length=1)


class ModeratorOut(BaseModel):
    community_id: str
    user_id: str
    role: str

    class Config:
        from_attributes = True


# ----------------
# Rules
# ----------------
class RuleIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    text: str = Field(...,min_length=1, max_length=500)


class RuleOut(BaseModel):
    id: str
    order: int
    title: str
    text: str

    class Config:
        from_attributes = True
