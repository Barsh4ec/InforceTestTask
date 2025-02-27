from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(UserCreate):
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
