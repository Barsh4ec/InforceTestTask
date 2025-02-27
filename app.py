
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship



DATABASE_URL = "postgresql://user:password@db/lunch_voting"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    menus = relationship("Menu", back_populates="restaurant")

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    date = Column(Date, default=date.today)
    items = Column(String)
    restaurant = relationship("Restaurant", back_populates="menus")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"))


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


