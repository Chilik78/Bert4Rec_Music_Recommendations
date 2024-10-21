from fastapi import APIRouter, Request

history_router = APIRouter()

@history_router.get('/select')
def select_route():
    ...
    
@history_router.delete('/delete')
def delete_route(id:str):
    ...
    
@history_router.put('/update')
def update_route(old, new):
    ...
    
@history_router.post('/insert')
def insert_route(new):
    ...