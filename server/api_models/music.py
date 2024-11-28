from pydantic import BaseModel

class Music(BaseModel):
    id:str
    trackName:str
    trackAuthor:str
    genre:str

class InsertMusic(BaseModel):
    trackName:str
    trackAuthor:str
    genre:str
    
class DownloadMusic(BaseModel):
    trackName:str
    trackAuthor:str