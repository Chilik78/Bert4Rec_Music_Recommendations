from fastapi import APIRouter

from api.database.Database import Database
from server.api_models.user import InsertUser, User

user_router = APIRouter()

db = Database()

def createUser(data):
    return User(**{k: v for k, v in zip(User.model_fields.keys(), data)})

@user_router.get('/select')
def select_route():
    users_data = db.getAllRecordsTable('user')
    users = list(map(createUser, users_data))
    return users

@user_router.post('/insert')
def insert_route(new_user:InsertUser):
    vals = tuple(new_user.model_dump()[key] for key in InsertUser.model_fields.keys())
    db.insertDataInUser(vals)
    
@user_router.get('/is_exist')
def is_exist_route(id:str):
    return db.is_exist(id, 'user')