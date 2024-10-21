from database.Database import Database
import pandas as pd
import csv

path = 'Database/data'

def upload_data():
    df_user_info = pd.read_csv(f'{path}/user_info.csv', encoding='UTF8')
    df_hisroty_of_listening = pd.read_csv(f'{path}/history_of_listening.csv', encoding='UTF8')
    df_users_ID = pd.read_csv(f'{path}/users.csv', encoding='UTF8')
    
    db = Database(pathDataBase=path)
    print(db)

    # Добавление пользователей в БД
    user_names = df_user_info['name'].tolist()
    user_passwords = df_user_info['password'].tolist()
    user_emails = df_user_info['email'].tolist()
    phone_number = df_user_info['phone_number'].tolist()

    for i in range(100):
        db.insertDataInUser((user_names[i], phone_number[i], user_emails[i], user_passwords[i]))
    
    
    # Добавление музыки в БД
    user_names_csv = df_hisroty_of_listening['userid'].tolist()
    track_names = df_hisroty_of_listening['track'].tolist()
    artist_names = df_hisroty_of_listening['artist'].tolist()
    track_genres = df_hisroty_of_listening['genre'].tolist()

    for i in range(1638):
        db.insertDataInMusic((track_names[i], artist_names[i], track_genres[i]))
    
    # Получение списка Id пользователей из БД
    users_id = db.getAllUserId()
    users_id_db = list()

    for user in users_id:
        user_id = user[0]
        users_id_db.append(user_id)

    # Получение списка Id музыки из БД
    musics_id = db.getAllMusicId()
    musics_id_db = list()

    for music in musics_id:
        music_id = music[0]
        musics_id_db.append(music_id)
    
    # Создание csv файла - ID Пользователя из CSV, ID музыки из БД
    with open(f'{path}/user_music_id.csv', mode='w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter= ",", lineterminator="\r")
        file_writer.writerow(["userid", "musicid"])
        for i in range(1638):
            file_writer.writerow([user_names_csv[i], musics_id_db[i]])

    # Получение списка Id пользователей из users.csv
    users_id_csv = df_users_ID['userid'].tolist()
    user_id_tuple = list()
    
    # Подготовка csv файла
    user_music_id = pd.read_csv(f'{path}/user_music_id.csv', encoding='UTF8')

    # Создание кортежа (Id пользователя из БД, Id пользователя из history_of_listening.csv)
    for i in range(100):
        user_id_tuple.append((users_id_db[i], users_id_csv[i])) 

    # Создание кортежа (Id пользователя из user_music.csv, Id музыки из history_of_listening.csv)
    user_id_for_tuple = user_music_id['userid'].to_list()
    music_id_for_tuple = user_music_id['musicid'].to_list()
    music_user_tuples = list()

    for i in range(1638):
       music_user_tuples.append((user_id_for_tuple[i], music_id_for_tuple[i]))
   
    # Добавление истории прослушивания в БД
    for user_id in user_id_tuple:
        for i in range(1638):
            if(user_id[1] == music_user_tuples[i][0]):
                db.insertDataInHistory((user_id[0], music_user_tuples[i][1]))

    #print(db.getAllRecordsTable('user'))
    #print(db.getAllRecordsTable('music'))
    #print(db.getAllRecordsTable('history'))
    
    print(db.getDataBaseName, db.getPathName, db.getTablesName)