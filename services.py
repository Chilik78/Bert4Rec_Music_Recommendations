from api.database.Database import Database
from api.recommendation_system.RecommSystem import RecommSystem
from api.recommendation_system.GeneratorData import GeneratorData

db = Database()
rs = RecommSystem(use_logging=True)
gd = GeneratorData()
