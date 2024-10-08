from certifi import contents
from pydantic import BaseModel, EmailStr, conint, ConfigDict
from pydantic.types import conint
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # class Config:
    #     from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # model_config = ConfigDict(arbitrary_types_allowed=True)
class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str

    # model_config = ConfigDict(arbitrary_types_allowed=True)
    class Config:
        from_attributes = True