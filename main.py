from fastapi import FastAPI
from server.api_routes import *

app = FastAPI()




app.include_router(user_router, prefix='/users')
app.include_router(music_router, prefix='/music')
app.include_router(history_router, prefix='/history')