from pydantic import BaseModel

class Music(BaseModel):
    id:str
    track:str
    artist:str
    genre:str

class InsertMusic(BaseModel):
    track:str
    artist:str
    genre:str
    
class DownloadMusic(BaseModel):
    track:str
    artist:str