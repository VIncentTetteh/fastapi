from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint



class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    id: int
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class PostVote(PostBase):
    Post: Post
    votes: int

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[str]


class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)