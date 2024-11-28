from api.database.Database import Database
from api.recommendation_system.RecommSystem import RecommSystem
from api.recommendation_system.GeneratorData import GeneratorData
from api.getting_music import SongDownloader

db = Database()
rs = RecommSystem(use_logging=True)
gd = GeneratorData()
sd = SongDownloader('server/files')
