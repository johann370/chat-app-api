from typing import List, Set, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class ServerBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ServerIn(ServerBase):
    pass


class ServerOut(ServerBase):
    owner_id: int
    owner: UserOut
    members: List[UserOut]


class Member(BaseModel):
    user_id: int
    server_id: int

    class Config:
        orm_mode = True


class MemberOut(Member):
    user: UserOut


class Message(BaseModel):
    content: str


class MessageIn(Message):
    pass


class MessageOut(Message):
    server_id: int
    timestamp: datetime
    author: UserOut

    class Config:
        orm_mode = True
