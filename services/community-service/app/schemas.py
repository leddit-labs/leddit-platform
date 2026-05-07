from pydantic import BaseModel, Field


class CommunityCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    description: str = Field(default="", max_length=500)


class CommunityUpdate(BaseModel):
    description: str | None = None


class CommunityOut(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        from_attributes = True
