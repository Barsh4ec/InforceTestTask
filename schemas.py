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


class UserOut(UserCreate):
    id: int
    email: EmailStr
    full_name: str


class EmployeeCreate(BaseModel):
    username: str
    password: str


class RestaurantCreate(BaseModel):
    name: str


class MenuCreate(BaseModel):
    restaurant_id: int
    items: str


class VoteCreate(BaseModel):
    employee_id: int
    menu_id: int
