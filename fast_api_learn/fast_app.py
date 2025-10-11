from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# FastAPI objesi (uvicorn bunu arayacak!)
app = FastAPI()

# Kullanıcı modeli
class User(BaseModel):
    id: int
    name: str
    email: str

# Basit veri deposu (RAM’de)
users: List[User] = []

# Kullanıcıları listeleme
@app.get("/users/", response_model=List[User])
async def get_users():
    return users

# Yeni kullanıcı ekleme
@app.post("/users/", response_model=User)
async def add_user(user: User):
    users.append(user)
    return user