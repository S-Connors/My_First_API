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

#get returns things
@app.get("/")
async def root():
    return {"Hello":"Welcome to my API"}

#this returns all users
@app.get("/users")
async def all_users():
    return db

#post adds new things
@app.post("/users/new")
async def new_user(user: User):
    db.append(user)
    return {"id":user.id}

#deletes users by user id
@app.delete("/users/delete/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return {f"User id: {user_id}":"Has been removed."}
    raise HTTPException(status_code=404, detail=f"User id: {user_id} does not exist.")

#put edits things
#changes user first, last, middle name etc.
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

#search by path first and last name
@app.get("/users/{user_first}/{user_last}")
async def user_by_full_name(user_first:str = Path(None, description="The first name of the person you are looking for."), user_last:str = Path(None, description="The last name of the person you are looking for.")):
    for user in db:
        if user.first_name == user_first and user.last_name == user_last:
            return [user for user in db if user.first_name == user_first and user.last_name == user_last]
    raise HTTPException(status_code=404, detail=f"User name: {user_first} {user_last} not found.")

#search by path first name
@app.get("/users/{user_name}")
async def user_by_first_name(user_name:str = Path(None, description="The first name of the person you are looking for.")):
    for user in db:
        return [user for user in db if user.first_name == user_name]
    raise HTTPException(status_code=404, detail=f"User name: {user_name} not found.")

#this is not working.....
#removed / from they/them pronouns as wouldnt work in path
#search by path pronoun
@app.get("/users/{pronoun}")
async def user_by_pronoun(
        pronoun:Pronouns = Path(None, description="The pronoun the person wishes to be called.")
    ):
    for user in db:
        return [user for user in db if user.pronouns == pronoun]
    raise HTTPException(status_code=404, detail=f"Pronoun: {pronoun} not found.")

#this is not working...
#search by query roles
@app.get("/users")
async def user_by_role(role:Role = Query(None, description="The role you wish to look up.")):
    for user in db:
        return [user for user in db if user.roles == role]
    raise HTTPException(status_code=404, detail=f"No one with {role} found.")

#this is not working...
#search by query first name
@app.get("/users")
async def search_users(user_first:str = Query(None, description= "The users first name."), user_last: Optional[str] = Query(None, max_length= 15, description = "The users last name.")):
    for user in db:
        return [user for user in db if user.first_name == user_first and user.last_name == user_last]
    else:
        return [user for user in db if user.first_name == user_first]






















    #
