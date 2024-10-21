from database.Database import Database
from data.upload_data_in_db import upload_data

def start():
    db = Database(pathDataBase='Database/data')
    print(db)

    # Загрузка всех данных в БД
    upload_data()
    
    #db.clearTable('user')
    #db.clearTable('history')
    #db.clearTable('music')
    #db.dropTable('user')
    #db.insertDataInUser(("name", "12345", "ggggg", 'pass'))
    #db.insertDataInMusic(("track", 'artist', 'gemre'))
    #db.insertDataInHistory(("429be54a-4e31-4914-820f-e1eb19156c4a", "2ed226e6-e269-40c6-8571-a1ceb52279df"))
    
    #print(db.getAllRecordsTable('user'))
    #print(db.getAllRecordsTable('music'))
    #print(db.getAllRecordsTable('history'))
    
    print(db.getDataBaseName, db.getPathName, db.getTablesName)