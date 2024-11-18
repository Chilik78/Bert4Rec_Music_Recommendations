from database.Database import Database
import uuid

def start():
    db = Database()
    
    #print(db)
    db.dropTable('convallid')
    
    # df = pd.read_csv('api\\songs_normalize.csv', encoding='utf-8')
    # df.drop(['duration_ms', 'explicit', 'year', 'popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'], axis=1, inplace=True)

    # print(df)

    # artist_names = []
    # song_names = []
    # genres = []

    # artist_names = df['artist'].to_list()
    # song_names = df['song'].to_list()
    # genres = df['genre'].to_list()  

    # for i in range(2000):
    #     db.insertDataInMusic((f"{song_names[i]}", f"{artist_names[i]}", f"{genres[i]}"))
        
    # db.dropTable('user')
    # db.insertDataInUser(("name", "12345", "ggggg", 'pass'))
    # db.insertDataInMusic(("track", 'artist', 'gemre'))
    # db.insertDataInHistory(("429be54a-4e31-4914-820f-e1eb19156c4a", "2ed226e6-e269-40c6-8571-a1ceb52279df"))
    
    # print(db.getAllRecordsTable('user'))
    # print(db.getAllRecordsTable('music'))
    # print(db.getAllRecordsTable('history'))
    
    # print(db.getDataBaseName, db.getPathName, db.getTablesName)

    # music_genre = db.getAllUniqValuesFromTablesColumn('music','genre')
    # result = []
    # for genre in music_genre:
    #     result.append(genre[0])
    # print(result)

    # res = db.is_exist_in_column('0cd0eda4-9dd7-4adf-be49-82b242811a53', 'history','user_id')
    # result = res[0]
    # print(result)
    
    # res = db.select_last_entry('history','user_id', 'music_id', 'fcdf7d44-8d05-4489-a0f5-624695a6ca9a')
    # result = res[1]
    # print(result)
    
    #db = Database()
    # res1 = db.is_exist_by_value('user', 'phone_number ', '12345')
    # res2 = db.is_exist_by_value('user', 'password', '12345')
    # print(res1 and res2)

def model_test():
    rs = RecommSystem()
    res = rs.do_predict()
    print(res)

if __name__ == '__main__':
    #gd = GeneratorData()
    #gd.change_history(148, [238, 138, 191, 20, 19, 30, 50])
    model_test()

