from fastapi import FastAPI
from routes import apiRtr

app = FastAPI()

app.include_router(apiRtr)

