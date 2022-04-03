from typing import Optional, List
#this libray gives unique ids
from uuid import UUID, uuid4
from pydantic import BaseModel
#enumerations are a set of symbolic names bound to unique, constant values
from enum import Enum

class Pronouns(str, Enum):
    he = "he/him"
    she = "she/her"
    they = "they/them"
    zir = "ze/zir"
    xe = "xe/xem"
    hir = "ze/hir"
    per = "per"
    na = "do not wish to disclose"

class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    student = "student"
    trial_user = "trial_user"
    user = "user"

#class our basemodel for all added data
class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]=None
    pronouns: Pronouns
    roles: List[Role]

class Updated(BaseModel):
    first_name: Optional[str]= None
    last_name: Optional[str]= None
    middle_name: Optional[str]= None
    pronouns: Optional[Pronouns]= None
    roles: Optional[List[Role]]= None
