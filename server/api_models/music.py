from pydantic import BaseModel

class Music(BaseModel):
    id:str
    track:str
    artist:str
    genre:str