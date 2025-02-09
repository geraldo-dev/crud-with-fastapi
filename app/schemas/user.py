from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50,
                      description='o nome do usuário')
    email: EmailStr = Field(..., description='A valid email address')


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=4,
        max_length=20,
        description='Password must be between 4 and 20 characters long'
    )


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdatePartial(BaseModel):
    name: str | None = Field(
        None, min_length=2, max_length=50, description="update name")
    email: EmailStr | None = Field(None, description="update email")
    password: str | None = Field(
        None, min_length=4, max_length=20, description="update password")
