from datetime import datetime, date, timedelta, timezone
import os

from schemas import UserCreate, TokenData
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.models import User, Restaurant, Menu, Vote


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_data(db: Session, form_username: str):
    user_data = db.execute(select(User).where(User.username == form_username)).scalar_one_or_none()
    return user_data


def get_user(user_data, username: str):
    if username == user_data.username:
        return user_data


def authenticate_user(user_data, username: str, password: str):
    user = get_user(user_data, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(User, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserCreate, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_restaurant(db: Session, name: str):
    restaurant = db.query(Restaurant).filter(Restaurant.name == name).first()
    return restaurant


def get_menu(db: Session):
    menu = db.query(Menu).filter(Menu.date == date.today()).all()
    return menu


def get_results_today(db: Session):
    results = (
        db.query(Menu.restaurant_id, func.count(Vote.id).label("votes"))
        .join(Vote, Vote.menu_id == Menu.id)
        .filter(Menu.date == date.today())
        .group_by(Menu.restaurant_id)
        .all()
    )
    return results
