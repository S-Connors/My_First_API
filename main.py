import uvicorn
from typing import Optional, List, Union, Any
from fastapi import FastAPI, Path, Query, HTTPException
from uuid import UUID

from pydantic import Field
from models import User, Pronouns, Role, UpdateRequest, UserRequestModel


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


# -----------------------------------------------------


# Create a single endpoint with query models
@app.get("/v2/users")
def get_user_with_query_model(
        first_name: Optional[str] = Query(
            default = None,
            title = 'First Name',
            description = 'The first name of the person you are searching for. '
                'Case sensitive',
            example = 'Stephanie',
            max_length=100
        ),
        middle_name: Optional[str] = Query(
            default = None,
            title = 'Middle Name',
            description = 'The middle name of the person you are searching for. '
                'Case sensitive',
            max_length=100
        ),
        last_name: Optional[str] = Query(
            default = None,
            title = 'Last Name',
            description = 'The last name of the person you are searching for. '
                'Case sensitive',
            example='connors',
            max_length=100
        ),
        pronouns: Optional[List[Pronouns]] = Query(
            default = None,
            title = 'Pronouns',
            description = 'Pronoun of the person you are searching for.'
                'Accepts a single value or a list of values',
            example=Pronouns('she')
        ),
        roles: Optional[List[Role]] = Query(
            default = None,
            title = 'Roles',
            description = 'Role of the person you are searching for. '
                'Accepts a single value or a list of values',
            example=Role('admin')
        ),
        limit: int = Query(
            default = 10,
            title = 'Limit',
            description = 'Limit the number of returned results',
            example = 10,
            gt = 1
        )
    ):
    """
    Returns all users which meet an exact match to the parameters
    passed in the query model. (Case sensitive.)
    """
    query_model = UserRequestModel(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        pronouns=pronouns,
        roles=roles,
        limit=limit
    )
    return post_user_with_query_model(query_model)



# Create a single endpoint with query models
@app.post("/v2/users")
def post_user_with_query_model(query_model: UserRequestModel):
    """
    Returns all users which meet an exact match to the parameters
    passed in the query model. (Case sensitive.)

    Functionality of this code is complex
    """
    all_users = []
    for field in User.__fields__.keys():

        # Skip fields which dont match
        if not hasattr(query_model, field):
            continue

        # Skip empty fields
        if not getattr(query_model, field):
            continue

        if not isinstance(getattr(query_model, field), list):
            # make sure all users match
            all_users = [x for x in all_users if getattr(x, field) == getattr(query_model, field)]

            # New people who match
            new_users = [x for x in db if getattr(x, field) == getattr(query_model, field)]

        else:
            for value in getattr(query_model, field):
                # What if the attribute is an array?

                # make sure all users match
                all_users = [x for x in all_users if helper_function_match(x, field, value)]

                # New people who match
                new_users = [x for x in db if helper_function_match(x, field, value)]

        # Remove those who already exist
        new_users = [x for x in new_users if x not in all_users]
        all_users += new_users

    return all_users

def helper_function_match(my_user: User, field: str, value: Any):
    """Compares a single value with either a single value or a list of values"""
    my_value = getattr(my_user, field)

    if isinstance(my_value, list):
        return value in my_value
    else:
        print(my_user, my_value, value, value in my_value)
        return value == my_value

# -------------------------------------



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
