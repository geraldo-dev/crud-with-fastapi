from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdatePartial(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
