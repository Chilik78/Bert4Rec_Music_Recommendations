from Database import Database
import hashlib

class Bridge():
    '''
        Класс моста между БД и Bert4Rec.
        Главная задача - быть конвертером для айдишников из string в int
        -----------------------------------

        Объект Класса Bridge

        Содержит:

            ---------------

    '''
    def __init__(self, db=Database()) -> None:
        self.__db = db

    def getAllHistory(self) -> tuple:
        '''Функция получения всех данных таблицы history
        
        '''

        tupleDB = self.__db.getAllRecordsTable('history')

        return self.getHashTuple(tupleDB)
    
    def getUserHistory(self, userId) -> tuple:
        '''Функция получения истории одного пользователя
        
            Параметры:
             ----------
             userId - айдишник пользователя
        
        '''

        tupleDB = self.__db.getValuesFromTableById('history', 'user_id', userId)

        return self.getHashTuple(tupleDB)
    
    def getHashTuple(self, tupleDB: tuple) -> tuple:
        result = []
        for val in tupleDB:
            hash_int_user = int.from_bytes(hashlib.sha256(val[0].encode()).digest()[:1], 'big')
            hash_int_music = int.from_bytes(hashlib.sha256(val[1].encode()).digest()[:1], 'big')
            result.append(( hash_int_user, hash_int_music))
        return result    
     