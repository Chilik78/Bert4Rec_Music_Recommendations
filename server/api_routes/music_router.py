from fastapi import APIRouter, Request

from api.database.Database import Database
from server.api_models.music import InsertMusic, Music

music_router = APIRouter()

db = Database()

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