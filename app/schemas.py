from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass
