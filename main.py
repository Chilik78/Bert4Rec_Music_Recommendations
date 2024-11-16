from fastapi import FastAPI
from server.api_routes import *
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(user_router, prefix='/users')
app.include_router(music_router, prefix='/music')
app.include_router(history_router, prefix='/history')

if __name__ == '__main__':
    uvicorn.run(app)