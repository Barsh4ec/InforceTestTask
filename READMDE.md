# Restaurant Menu Vote API🍽️
___

This API helps employees decide where to eat lunch by allowing restaurants to upload daily menus and employees to vote for them. The backend supports multiple app versions via build version headers.

## Installation
___

Python3 must be already installed.
- Create a .env file using .env.sample and specify environment variables inside the .env to run the project with Docker.

```shell
git clone https://github.com/Barsh4ec/InforceTestTask.git
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
fastapi dev app.py # or uvicorn app:app --host 127.0.0.1 --port 8000
```

## Run with Docker
___

To run the project using Docker, follow these steps:

- Run the following command to build and start the Docker containers:
```shell
docker-compose up --build
```

## Features based on user role
___
### 🔐 Authentication

User registration with hashed passwords  
JWT-based authentication for secure access

### 🏢 Restaurants Management

Create restaurants

### 📜 Menu Management
Upload menus – Each restaurant can upload a daily menu  
Get today’s menu – Employees can view available menus

### 🗳️ Voting System
Vote for a menu – Employees can vote once per day  
View voting results – Aggregated votes for the current day

### For creating new account follow these endpoints:
- Create user - /users/create
- Get access token - /token


## Endpoints Overview
### Authentication
✅ POST /register – Register a new employee

### Restaurants
✅ POST /restaurants – Create a restaurant (Prevents duplicates)

### Menus
✅ POST /menus – Upload a menu for a restaurant  
✅ GET /menus/today – Get menus for the current day

### Voting
✅ POST /vote – Employees can vote (Only once per day)  
✅ GET /results – Get voting results for today



## Technologies
___
FastAPI  
SQLAlchemy  
Pydantic  
PostgreSQL  
Alembic  
uvicorn  
Docker