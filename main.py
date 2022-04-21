#run this in terminal to auto load
#python main.py
#Press CTRL+C to quit
#go to http://127.0.0.1:8000

import uvicorn
from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException
from uuid import UUID

from models import User, Pronouns, Role, UpdateRequest


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
    id = UUID("5b2cba3a-c3ba-4c12-9042-16cbd90054b9"),
    first_name = "jen",
    last_name = "jacobs",
    pronouns = Pronouns.they,
    roles = [Role.student, Role.trial_user])
]

#get returns things
@app.get("/")
def root():
    return {"Hello":"Welcome to my API"}

#this returns all users
@app.get("/users/all")
def all_users():
    return db

#post adds new things
@app.post("/users/new")
def new_user(user: User):
    db.append(user)
    return user

#deletes users by user id
@app.delete("/users/delete/{user_id}")
def delete_user(user_id:UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return {f"User id: '{user_id}'has been removed."}
    raise HTTPException(
        status_code = 404,
        detail = f"User id: '{user_id}' does not exist."
    )

#put edits things
#changes user first, last, middle name etc.
@app.put("/users/update/{user_id}")
def update_user(updated: UpdateRequest, user_id: UUID):
    for user in db:
        if user_id == user.id:
            if updated.first_name != None:
                user.first_name = updated.first_name
            if updated.last_name != None:
                user.last_name = updated.last_name
            if updated.middle_name != None:
                user.middle_name = updated.middle_name
            if updated.pronouns != None:
                user.pronouns = updated.pronouns
            if updated.roles != None:
                user.roles = updated.roles
            return user
    raise HTTPException(
        status_code = 404,
        detail = f"User id: '{user_id}' does not exist."
    )

#ask about standardized/ best practice spacing?? each parameter gets new line??
#search by path first and last name
@app.get("/users/fullname{user_first}/{user_last}")
async def user_by_full_name(
    user_first:str = Path(
    None,
    description = "The first name of the person you are looking for."
    ),
    user_last:str = Path(
    None,
    description = "The last name of the person you are looking for."
    )
):
    for user in db:
        if user.first_name == user_first and user.last_name == user_last:
            return [user for user in db if user.first_name == user_first and user.last_name == user_last]
    raise HTTPException(
        status_code = 404,
        detail = f"User name: '{user_first} {user_last}' not found."
    )

#search by path first name
@app.get("/users/first/{user_name}")
def user_by_first_name(
    user_name:str = Path(None,
    description = "The first name of the person you are looking for.")
):
    for user in db:
        if user.first_name == user_name:
            return [user for user in db if user.first_name == user_name]
    raise HTTPException(
    status_code=404,
    detail=f"User name: '{user_name}' not found."
    )


#search by path pronoun
@app.get("/users/pronoun/{pronoun}")
def user_by_pronoun(
        pronoun:Pronouns = Path(...,
        discription = "The pronoun the person wishes to be called")
    ):
    for user in db:
        if user.pronouns == pronoun:
            return [user for user in db if user.pronouns == pronoun]
    raise HTTPException(
        status_code = 404,
        detail = f"Pronoun: '{pronoun}' not found."
    )

# search by path roles
@app.get("/users/role/{user_role}")
def user_by_role(
    user_role:Role = Path(..., description = "The role you wish to look up.")
):
    for user in db:
        if user_role in user.roles:
            return [user for user in db if user_role in user.roles]
    raise HTTPException(
        status_code = 404,
        detail = f"Role: '{user_role}' not found."
    )


#search by path user id
@app.get("/users/id/{user_id}")
def user_by_user_id(
    user_id:UUID = Path(..., discription = "The users id")
):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code = 404,
        detail = f"User ID: '{user_id}' not found"
    )



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
