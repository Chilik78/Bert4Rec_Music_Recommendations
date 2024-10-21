from fastapi import FastAPI
from server.api_routes import *

app = FastAPI()


'''
- Все жанры music
- Первый ли раз зашёл в приложение history
- Последняя песня, которую слушал чел history
'''

app.include_router(user_router, prefix='/users')
app.include_router(music_router, prefix='/music')
app.include_router(history_router, prefix='/history')