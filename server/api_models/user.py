from pydantic import BaseModel

class User(BaseModel):
    id:str
    name:str
    phone:str
    email:str
    password:str
    
class InsertUser(BaseModel):
    name:str
    phone:str
    email:str
    password:str