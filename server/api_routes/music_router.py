from fastapi import APIRouter, Request

music_router = APIRouter()

@music_router.get('/select')
def select_route():
    ...

@music_router.delete('/delete')
def delete_route(id:str):
    ...
    
@music_router.put('/update')
def update_route(old, new):
    ...

@music_router.post('/insert')
def insert_route(new):
    ...