#run this in terminal to auto load
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
    first_name = "stephanie",
    last_name = "connors",
    pronouns = Pronouns.she,
    roles = [Role.admin, Role.user]),
User(
    id =UUID("5b2cba3a-c3ba-4c12-9042-16cbd90054b9"),
    first_name = "jen",
    last_name = "jacobs",
    pronouns = Pronouns.they,
    roles = [Role.student, Role.trial_user])
]

@app.get("/")
async def root():
    return {"Hello":"Welcome to my API"}

@app.get("/users")
async def all_users():
    return db

@app.post("/users/new")
async def new_user(user: User):
    db.append(user)
    return {"id":user.id}

@app.delete("/users/delete/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return {f"User id: {user_id}":"Has been removed."}
    raise HTTPException(status_code=404, detail=f"User id: {user_id} does not exist.")

@app.put("/users/update/{user_id}")
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

@app.get("/users/{user_first}/{user_last}")
async def user_by_name(user_first:str = Path(None, description="The first name of the person you are looking for."), user_last:str = Path(None, description="The last name of the person you are looking for.")):
    for user in db:
        if user.first_name == user_first and user.last_name == user_last:
            return [user for user in db if user.first_name == user_first and user.last_name == user_last]
    raise HTTPException(status_code=404, detail=f"User name: {user_name} {user_last} not found.")

@app.get("/users/{user_name}")
async def user_by_name(user_name:str = Path(None, description="The first name of the person you are looking for.")):
    for user in db:
        if user.first_name == user_name:
            return [user for user in db if user.first_name == user_name]
    raise HTTPException(status_code=404, detail=f"User name: {user_name} not found.")

@app.get("/users/{pronoun}")
async def user_by_pronoun(pronoun:Pronouns = Path(None, description="The pronouns the person wishes to be called.")):
    for user in db:
        if user.pronouns == pronoun:
            return [usuer for user in db if user.pronouns == pronoun]
    raise HTTPException(status_code=404, detail=f"Pronoun: {pronoun} not found.")

@app.get("/users/{role}")
async def user_by_role(role:Role = Path(None, description="The role you wish to look up.")):
    for user in db:
        if user.roles == role:
            return [usuer for user in db if user.roles == role]
    raise HTTPException(status_code=404, detail=f"No one with {role} found.")






















    #
