from fastapi import APIRouter
from api.database.Database import Database

history_router = APIRouter()

db = Database()

@history_router.get('/is_first_entry')
def select_route(user_id:str):
    status = db.is_exist_in_column(user_id,'history','user_id')
    result = status[0]
    return result == 1
    
@history_router.get('/select_user_last_music')
def select_route(user_id:str):
    res = db.select_last_entry('history','user_id', 'music_id', user_id)
    result = res[1]
    return result