import sqlite3
from Database import Database

class Bridge():
    '''
        Класс моста между БД и Bert4Rec.
        Главная задача - быть конвертером для айдишников из string в int
        -----------------------------------

        Объект Класса Bridge

        Содержит:

            ---------------

    '''
    def __init__(self) -> None:
        self.__db = Database()

    def getAllHistory(self) -> tuple:
        '''Функция получения всех данных таблицы history
        
        '''
        
        tupleDB = self.__db.getAllRecordsTable('history')
        result = []

        for i in tupleDB:
            firstVal = int(i[0].replace('-', ''), 32)
            secondVal = int(i[1].replace('-', ''), 32)
            result.append((firstVal, secondVal))

        return result
    
    def getUserHistory(self, userId) -> tuple:
        '''Функция получения истории одного пользователя
        
            Параметры:
             ----------
             userId - айдишник пользователя
        
        '''
        tupleDB = self.__db.getValuesFromTableById('history','user_id', userId)
        result = []
        
        for i in tupleDB:
            firstVal = int(i[0].replace('-', ''), 32)
            secondVal = int(i[1].replace('-', ''), 32)
            result.append((firstVal, secondVal))

        return result