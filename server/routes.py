from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sqlite3
import uuid
apiRtr = APIRouter()

conn = sqlite3.connect('MusicGuru.db')
cursor = conn.cursor()

@apiRtr.post("/user")
async def create_user(name:str, phone_number:str, email:str, password:str):
    try:
        uid = str(uuid.uuid4())
        sql = f"INSERT INTO user (id, name, phone_number, email, password) VALUES ('{uid}', ?, ?, ?, ?)"
        cursor.execute(sql, (name, phone_number, email, password))
        conn.commit()
        return JSONResponse(status_code=201, content={"message": "Пользователь создан"})
    except Exception as e:
        print(f"Ошибка исполнения: {e}")

@apiRtr.post("/music")
async def create_music_data(track:str, artist:str, genre:str):
    try:
        uid = str(uuid.uuid4())
        sql = f"INSERT INTO music (id, track, artist, genre) VALUES ('{uid}', ?, ?, ?)"
        cursor.execute(sql, (track, artist, genre))
        conn.commit()
        return JSONResponse(status_code=201, content={"message": "Трек добавлен"})
    except Exception as e:
        print(f"Ошибка исполнения: {e}")


# @apiRtr.post("/history")
# async def create_music_data(track:str, artist:str, genre:str):
#     try:

#     except Exception as e:
#         print(f"Ошибка исполнения: {e}")


@apiRtr.get("/user/{user_id}")
async def get_user(user_id: str):
    try:
        sql = "SELECT * FROM users WHERE user_id = ?"
        cursor.execute(sql, (user_id))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Ошибка исполнения: {e}")


@apiRtr.get("/music/{music_id}")
async def get_user(music_id: str):
    try:
        sql = "SELECT * FROM music WHERE music_id = ?"
        cursor.execute(sql, (music_id))
        music = cursor.fetchone()
        return music
    except Exception as e:
        print(f"Ошибка исполнения: {e}")


@apiRtr.get("/history")
async def get_user(user_id: str):
    try:
        sql = "SELECT * FROM history WHERE user_id = ?"
        cursor.execute(sql, (user_id))
        history = cursor.fetchone()
        return history
    except Exception as e:
        print(f"Ошибка исполнения: {e}")


@apiRtr.on_event("shutdown")
async def shutdown_db_connection():
    conn.close()