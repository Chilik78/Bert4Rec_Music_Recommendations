from fastapi import APIRouter

from services import db
from server.api_models.user import InsertUser, User

user_router = APIRouter()

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

@user_router.get('/is_exist_by_values')
def is_exist_route(columnName: str, value, password):
    res1 = db.is_exist_by_value('user', columnName, value)
    res2 = db.is_exist_by_value('user', 'password', password)
    res = res1 and res2
    userId = db.getIdByValue('user', columnName, value)
    return (res, userId[0])