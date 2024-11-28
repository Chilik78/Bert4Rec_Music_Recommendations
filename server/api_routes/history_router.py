from fastapi import APIRouter
from server.api_models.music import Music
from server.api_models.user import UserID
from services import db

history_router = APIRouter()

def createMusic(data):
    return Music(**{k: v for k, v in zip(Music.model_fields.keys(), data)})

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

@history_router.post('/get_all_tracks_user_history')
def get_all_tracks_user_history_route(obj:UserID) -> list[Music]:
    user_id = obj.user_id
    if not db.is_exist(user_id, 'user'): return
    vals = db.getValuesFromTableById('history', 'user_id', user_id)
    music_ids = [item[1] for item in vals]
    music_tuples = list(map(lambda id: db.getValuesFromTableById('music', 'id', id)[0], music_ids))
    musics = list(map(createMusic, music_tuples))
    return musics
    