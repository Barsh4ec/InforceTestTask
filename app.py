from datetime import date, timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_
from passlib.context import CryptContext
from typing import Annotated

from db.database import SessionLocal
from schemas import Token, UserCreate, UserOut, RestaurantCreate, MenuCreate, VoteCreate
from db.models import User, Restaurant, Menu, Vote
from crud import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user_data,
    get_restaurant,
    get_menu,
    get_results_today
)




ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    get_db()


@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)  # Inject database session
) -> Token:
    user_data = get_user_data(db, form_data.username)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(user_data, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=UserCreate)
async def read_users_me(
    current_user: Annotated[UserCreate, Depends(get_current_active_user)],
):
    return current_user


def hash_password(password: str):
    return pwd_context.hash(password)


@app.post("/users/create", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        disabled=False,
        full_name=user.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/restaurants")
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    existing_restaurant = get_restaurant(db, restaurant.name)
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant with this name already exists")

    db_restaurant = Restaurant(name=restaurant.name)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


@app.post("/menus")
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = Menu(restaurant_id=menu.restaurant_id, items=menu.items)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@app.get("/menus/today")
def get_today_menu(db: Session = Depends(get_db)):
    today_menus = get_menu(db)
    return today_menus


@app.post("/vote")
def vote(vote: VoteCreate, db: Session = Depends(get_db)):
    existing_vote = db.query(Vote).filter(
        and_(Vote.employee_id == vote.employee_id, Vote.date == date.today())
    ).first()

    if existing_vote:
        raise HTTPException(status_code=400, detail="You have already voted today")

    db_vote = Vote(employee_id=vote.employee_id, menu_id=vote.menu_id, date=date.today())
    db.add(db_vote)
    db.commit()
    return {"message": "Vote recorded"}


@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    results = get_results_today(db)

    return [{"restaurant_id": r.restaurant_id, "votes": r.votes} for r in results]
