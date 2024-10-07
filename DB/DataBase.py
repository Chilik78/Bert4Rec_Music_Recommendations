import sqlite3
import uuid

class DataBase():
    '''
        Класс Базы Данных Музыкального гуру
        -----------------------------------

        Объект Класса Базы Данных

        Содержит:

            `nameTable` - название таблицы в Базе Данных

        Таблицы БД:

            user - пользователь
            history - история прослушки
            music - вся музыка

    '''
    def __init__(self, nameDataBase:str = "MusicGuru.db") -> None:
        '''
            Конструктор Базы Данных Музыкального гуру

            Параметры:
            ----------
            
                `nameDataBase` - название Базы Данных (По умолчанию: "MusicGuru.db")

            ----------
        '''

        self.nameDataBase = nameDataBase
        '''Название Базы Данных'''
        self.tableNames = ['user','history','music']
        

        connection = sqlite3.connect(f"{nameDataBase}")
        cursor = connection.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS user(user_id, name, phone_number, email, password)").fetchone()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS music(music_id, track, artist, genre)").fetchone()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS history(user_id, music_id)").fetchone()

        connection.commit()

        connection.close()
        
    def insertDataOneInTable(self, tableName:str, data:list, user_id:str = '', music_id:str = '')->None:

        '''
            Функция вставки в таблицу данных одной строки

            Параметры:
            ----------
                `tableName` - название таблицы, в которую нужно добавить данные

                `data` - данные, которые необходимо вставить в новую запись

            Необязательные параметры, которые используются для таблицы 'history'

                'user_id' 
 
                'music_id' 

        '''

        con = sqlite3.connect(f'{self.nameDataBase}')

        cur = con.cursor()
        
        uid = str(uuid.uuid4())

        if(tableName == 'user'):
            cur.execute(f"INSERT INTO user (user_id, name, phone_number, email, password) VALUES ('{uid}','{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')").fetchall()
        elif(tableName == 'history'):
            cur.execute(f"INSERT INTO history (user_id, music_id) VALUES ('{user_id}','{music_id}')").fetchall()
        elif(tableName == 'music'):
            cur.execute(f"INSERT INTO music (music_id, track, artist, genre) VALUES ('{uid}', '{data[0]}', '{data[1]}', '{data[2]}')").fetchone()

        con.commit()

        con.close()

    def insertDataAllInTable(self, tableName:str, datas:list[list], user_id:list = [], music_id:list = []) -> None:
        '''
            Функция вставки в таблицу данных во множество строк

            Параметры:
            ----------

                `datas` - данные, которые необходимо вставить в новые записи
                
            Необязательные параметры, которые используются для таблицы 'history'

                'user_id' 
 
                'music_id' 

        '''

        con = sqlite3.connect(f"{self.nameDataBase}")

        cur = con.cursor()

        i = 0
        for data in datas:
            uid = str(uuid.uuid4())
            try:
                if(tableName == 'user'):
                    cur.execute(f"INSERT INTO user (user_id, name, phone_number, email, password) VALUES ('{uid}','{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')").fetchall()
                elif(tableName == 'history'):
                    cur.execute(f"INSERT INTO history (user_id, music_id) VALUES ('{user_id[i]}','{music_id[i]}')").fetchall()
                elif(tableName == 'music'):
                    cur.execute(f"INSERT INTO music (music_id, track, artist, genre) VALUES ('{uid}', '{data[0]}', '{data[1]}', '{data[2]}')").fetchone()
            except Exception as e:
                print(f"Ошибка добавления записи!!! - {data}\n")
            i += 1


        con.commit()

        con.close()

    def dropTable(self, tableName)->None:
        '''Функция удаления таблицы

            Параметры:
             ----------
             tableName - имя таблицы
        
        '''

        con = sqlite3.connect(f"{self.nameDataBase}")

        cur = con.cursor()

        if(tableName == 'user'):
            cur.execute(f"DROP TABLE IF EXISTS user").fetchone()
        elif(tableName == 'history'):
            cur.execute(f"DROP TABLE IF EXISTS history").fetchone()
        elif(tableName == 'music'):
            cur.execute(f"DROP TABLE IF EXISTS music").fetchone()

        con.commit()

        con.close()

    def clearTable(self, tableName)->None:
        '''Функция очищения таблицы

            Параметры:
             ----------
             tableName - имя таблицы
        
        '''

        con = sqlite3.connect(f"{self.nameDataBase}")

        cur = con.cursor()

        cur.execute(f"DROP TABLE IF EXISTS {tableName}").fetchone()

        if(tableName == 'user'):
            cur.execute(f"CREATE TABLE IF NOT EXISTS user(user_id, name, phone_number, email, password)").fetchone()
        elif(tableName == 'music'):
            cur.execute(f"CREATE TABLE IF NOT EXISTS music(music_id, track, artist, genre)").fetchone()
        elif(tableName == 'history'):
            cur.execute(f"CREATE TABLE IF NOT EXISTS history(user_id, music_id)").fetchone()
        
        con.commit()

        con.close()

    def getAllRecordsTable(self, tableName)->list:
        '''Функция получения всех данных таблицы
        
            Параметры:
             ----------
             tableName - имя таблицы
        
        '''

        con = sqlite3.connect(f"{self.nameDataBase}")

        cur = con.cursor()

        result = cur.execute(f"SELECT * FROM {tableName}").fetchall()

        con.commit()

        con.close()

        return result

    @property
    def getTablesName(self) -> list:
        '''Функция получения имен всех таблиц'''
        return self.tableNames
            