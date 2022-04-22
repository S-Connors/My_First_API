from uuid import UUID, uuid4
from enum import Enum

from typing import Optional, List, Union

from pydantic import BaseModel, Field, ValidationError, validator


#enumerations are a set of symbolic names bound to unique, constant values
class Pronouns(str, Enum):
    he = "he"
    she = "she"
    they = "they"
    zir = "zir"
    xe = "xe"
    hir = "hir"
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

class UpdateRequest(BaseModel):
    first_name: Optional[str]= None
    last_name: Optional[str]= None
    middle_name: Optional[str]= None
    pronouns: Optional[Pronouns]= None
    roles: Optional[List[Role]]= None


class UserRequestModel(BaseModel):
    """
    Request model for user endpoint.
    """
    first_name: Optional[str] = Field(
        default = None,
        title = 'First Name',
        description = 'The first name of the person you are searching for. '
            'Case sensitive',
        example = 'Stephanie',
        max_length=100
    )
    middle_name: Optional[str] = Field(
        default = None,
        title = 'Middle Name',
        description = 'The middle name of the person you are searching for. '
            'Case sensitive',
        max_length=100
    )
    last_name: Optional[str] = Field(
        default = None,
        title = 'Last Name',
        description = 'The last name of the person you are searching for. '
            'Case sensitive',
        example='connors',
        max_length=100
    )
    pronouns: Optional[Union[Pronouns, List[Pronouns]]] = Field(
        default = None,
        title = 'Pronouns',
        description = 'Pronoun of the person you are searching for.'
            'Accepts a single value or a list of values',
        example=Pronouns('she')
    )
    roles: Optional[Union[Role, List[Role]]] = Field(
        default = None,
        title = 'Roles',
        description = 'Role of the person you are searching for. '
            'Accepts a single value or a list of values',
        example=Role('admin')
    )
    limit: int = Field(
        default = 10,
        title = 'Limit',
        description = 'Limit the number of returned results',
        example = 10,
        gt = 1
    )

    # Let's say I want to be sure that no more than 3 pronouns are selected
    @validator('pronouns')
    def no_more_than_3_pronouns(cls, v):
        if v and isinstance(v, list) and len(v)>=3:
            raise ValueError('Cannot have more than 3 pronouns in one search')
        return v
