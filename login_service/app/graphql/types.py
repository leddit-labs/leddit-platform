import strawberry
from datetime import datetime
from typing import Optional
import enum 

@strawberry.enum
class UserRole(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

@strawberry.type
class UserProfile:
    id: int
    username: str
    email: str
    bio: Optional[str]
    karma: int
    role: UserRole
    created_at: datetime

@strawberry.type
class AuthPayload:
    access_token: str
    token_type: str

@strawberry.type
class Message:
    message: str

@strawberry.input
class RegisterInput:
    email: str
    username: str
    password: str

@strawberry.input
class LoginInput:
    username: str
    password: str