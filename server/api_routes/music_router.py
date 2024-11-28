from fastapi import APIRouter, Response
from services import db, rs, gd
from server.api_models.music import InsertMusic, Music
from server.api_models.user import UserID
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
def get_predicted_track_route(obj:UserID, response: Response) -> Music:
    response.headers['Access-Control-Allow-Origin'] = '*'
    user_id = obj.user_id
    if not db.is_exist(user_id, 'user'): return
    convhistory_by_id = db.getValuesFromTableById('convhistory', 'user_id', user_id)  
    turned_music_ids = list(map(lambda x: x[2], convhistory_by_id))
    turned_user_id = convhistory_by_id[0][0]
    gd.change_history(turned_user_id, turned_music_ids)
    gd.gen_files_for_train()
    gd.gen_file_for_predict()
    music_id = rs.do_predict()
    bd_music_id = db.getValuesFromTableById('convallid', 'conv_music_id', music_id)[0][1]
    music = db.getValuesFromTableById('music', 'id', bd_music_id)[0]
    return createMusic(music)