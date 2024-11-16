from fastapi import APIRouter

from api.database.Database import Database
from server.api_models.music import InsertMusic, Music
from random import choice

music_router = APIRouter()

db = Database()

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
    