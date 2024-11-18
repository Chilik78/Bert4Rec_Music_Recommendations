from fastapi import APIRouter

from services import db, rs, gd
from server.api_models.music import InsertMusic, Music
from random import choice

music_router = APIRouter()

def createMusic(data):
    return Music(**{k: v for k, v in zip(Music.model_fields.keys(), data)})

@music_router.get('/select_all_genres')
def select_route():
    music_genre = db.getAllUniqValuesFromTablesColumn('music','genre')
    result = []
    for genre in music_genre:
        result.append(genre[0])
    return result


@music_router.post('/insert')
def insert_route(new_music:InsertMusic):
    vals = tuple(new_music.model_dump()[key] for key in InsertMusic.model_fields.keys())
    db.insertDataInMusic(vals)
    
@music_router.post('/get_random_music')
def get_random_music_route(genres:list[str]) -> Music:
    genre = choice(genres)
    musics = db.getValuesFromTableById('music', 'genre', genre)
    res = choice(musics)
    return createMusic(res)
    
@music_router.post('/get_predicted_track')
def get_predicted_track_route(user_id:str) -> Music:
    history_by_id = db.getValuesFromTableById('history', 'user_id', user_id)
    music_ids = list(map(lambda x: x[1], history_by_id))
    #TODO: Здесь должна меняться история прослушивания, чтобы модель понимала для какого пользователя она прогнозирует
    #?turned_music_ids = Bridge.func(music_ids)
    #?turned_user_id = Bridge.func(user_id)
    #?gd.change_history(turned_user_id, turned_music_ids)
    
    music_id = rs.do_predict()
    #TODO: Сюда сделать перевод id и доставание музыки по нём
    #?bd_music_id = Bridge.func(music_id)
    bd_music_id = None(music_id)
    music = db.getValuesFromTableById('music', 'id', bd_music_id)[0]
    return music