#run this in terminal to autoreload
#uvicorn main:app --reload
#Press CTRL+C to quit
#go to http://127.0.0.1:8000

from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException
from uuid import UUID

from models import User, Pronouns, Role, Updated

#create instance of fastapi
app = FastAPI()

db: List[User] = [
User(
    id = UUID("f9c05069-e185-4f7b-ad45-1af3323098a7"),
    first_name = "Stephanie",
    last_name = "Connors",
    pronouns = Pronouns.she,
    roles = [Role.admin, Role.user]),
User(
    id =UUID("5b2cba3a-c3ba-4c12-9042-16cbd90054b9"),
    first_name = "Jen",
    last_name = "Jacobs",
    pronouns = Pronouns.they,
    roles = [Role.student, Role.trial_user])
]

@app.get("/")
async def root():
    return {"Hello":"Welcome to my API"}

@app.get("/users")
async def all_users():
    return db

@app.post("/users")
async def new_user(user: User):
    db.append(user)
    return {"id":user.id}

@app.delete("/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
        raise HTTPException(status_code=404, detail=f"User id: {user_id} does not exist.")

@app.put("/users/{user_id}")
async def update_user(user_id:UUID, updated: Updated):
    for user in db:
        if user.id == user_id:
            if user.first_name != None:
                user.first_name = updated.first_name
            if user.last_name != None:
                user.last_name = updated.last_name
            if user.middle_name != None:
                user.middle_name = updated.middle_name
            if user.pronouns != None: 
                user.pronouns = updated.pronouns
            if user.roles != None:
                user.roles = updated.roles
            return user
        raise HTTPException(status_code=404, detail=f"User id: {user_id} does not exist.")
