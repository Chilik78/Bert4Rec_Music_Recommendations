import sqlite3
import uuid

class Database():
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
    def __init__(self, nameDataBase:str = "MusicGuru.db", pathDataBase:str = "data") -> None:
        '''
            Конструктор Базы Данных Музыкального гуру

            Параметры:
            ----------
            
                `nameDataBase` - название Базы Данных (По умолчанию: "MusicGuru.db")

            ----------
        '''
        self.__databaseName = nameDataBase
        self.__databasePath = pathDataBase
        self.__tableNames = ['user','history','music']
        self.__create_tables()
    
    def __repr__(self):
        return f"Путь: {self.__databasePath}/{self.__databaseName}\nТаблицы: {', '.join(self.__tableNames)}"
    
    def insertDataInUser(self, params:tuple):
        '''params:
            - name
            - phone_number
            - email
            - password
        '''
        uid = str(uuid.uuid4())
        sql = f"INSERT INTO user (id, name, phone_number, email, password) VALUES ('{uid}', ?, ?, ?, ?)"
        self.__execute(sql, params)
        
    def insertDataInHistory(self, params:tuple):
        '''params:
            - user_id
            - music_id
        '''
        sql = f"INSERT INTO history (user_id, music_id) VALUES (?, ?)"
        self.__execute(sql, params)
        
    def insertDataInMusic(self, params:tuple):
        '''params:
            - track
            - artist
            - genre
        '''
        uid = str(uuid.uuid4())
        sql = f"INSERT INTO music (id, track, artist, genre) VALUES ('{uid}', ?, ?, ?)"
        self.__execute(sql, params)
        
    def __connect(self):
        return sqlite3.connect(f'{self.__databasePath}/{self.__databaseName}')
    
    def __many_execute(self, sql:str, params_list:list = []):
        try:
            con = self.__connect()
            cur = con.cursor()
            for params in params_list:
                if not params: cur.execute(sql)
                else: cur.execute(sql, params)
           
        except Exception as e:
            print(f"Ошибка исполнения: {e}")
        finally:
            con.commit()
            cur.close()
            con.close()
    
    def __execute(self, sql:str, params:tuple = ()):
        try:
            con = self.__connect()
            cur = con.cursor()
            if not params: cur.execute(sql)
            else: cur.execute(sql, params)
           
        except Exception as e:
            print(f"Ошибка исполнения: {e}")
        finally:
            con.commit()
            cur.close()
            con.close()
    
    def __fetch_all(self, sql:str, params:tuple = ()):
        try:
            con = self.__connect()
            cur = con.cursor()
            cur.execute(sql, params)
        except Exception as e:
            print(f"Ошибка исполнения: {e}")
        finally:
            result = cur.fetchall()
            con.commit()
            cur.close()
            con.close()
            return result
        
    def __fetch_one(self, sql:str, params:tuple = ()):
        try:
            con = self.__connect()
            cur = con.cursor()
            cur.execute(sql, params)
        except Exception as e:
            print(f"Ошибка исполнения: {e}")
        finally:
            result = cur.fetchone()
            con.commit()
            cur.close()
            con.close()
            return result
            
        
    def __create_user_table(self):
        sql = f"""CREATE TABLE IF NOT EXISTS user(
            id TEXT PRIMARY KEY, 
            name TEXT, 
            phone_number TEXT, 
            email TEXT, 
            password TEXT
            )"""
        self.__execute(sql)
        
    def __create_history_table(self):
        sql = f"""CREATE TABLE IF NOT EXISTS music(
            id TEXT PRIMARY KEY, 
            track TEXT, 
            artist TEXT, 
            genre TEXT
            )"""
        self.__execute(sql)
        
    def __create_music_table(self):
        sql = f"""CREATE TABLE IF NOT EXISTS history(
            user_id TEXT, 
            music_id TEXT, 
            FOREIGN KEY (user_id) REFERENCES user (user_id), 
            FOREIGN KEY (music_id) REFERENCES music (music_id)
            )"""
        self.__execute(sql)
        
    def __create_table(self, table_name:str):
        if table_name == 'user': self.__create_user_table()
        elif table_name == 'history': self.__create_history_table()
        elif table_name == 'music': self.__create_music_table()
        
    def __create_tables(self):
        for table in self.__tableNames: self.__create_table(table)

    def dropTable(self, tableName)->None:
        '''Функция удаления таблицы

            Параметры:
             ----------
             tableName - имя таблицы
        
        '''

        sql = f"DROP TABLE IF EXISTS {tableName}"
        self.__execute(sql)

    def clearTable(self, tableName)->None:
        '''Функция очищения таблицы

            Параметры:
             ----------
             tableName - имя таблицы
        
        '''
        self.dropTable(tableName)
        self.__create_table(tableName)
    
    def getAllUserId(self)->list:
        sql = f"SELECT id FROM user"
        result = self.__fetch_all(sql)
        return result
    
    def getAllMusicId(self)->list:
        sql = f"SELECT id FROM music"
        result = self.__fetch_all(sql)
        return result


    def getAllRecordsTable(self, tableName)->list:
        '''Функция получения всех данных таблицы
        
            Параметры:
             ----------
             tableName - имя таблицы
        
        '''
        sql = f"SELECT * FROM {tableName}"
        result = self.__fetch_all(sql)
        return result

    @property
    def getTablesName(self) -> list:
        '''Таблицы'''
        return self.__tableNames
    
    @property
    def getDataBaseName(self) -> str:
        '''Название DB'''
        return self.__databaseName
    
    @property
    def getPathName(self) -> str:
        '''Папка DB'''
        return self.__databasePath