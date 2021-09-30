from typing import Optional
from pydantic import BaseModel




class Blog(BaseModel):
    title : str
    body: str
    #published: Optional[bool]


class User(BaseModel):
    name: str
    email:str
    password: str


class ShowUser(BaseModel):
    name: str
    email:str

    class Config():
        orm_mode = True