from pydantic import BaseModel

from server.api_models.music import Music
from server.api_models.user import User

class History(BaseModel):
    user:User
    music:Music