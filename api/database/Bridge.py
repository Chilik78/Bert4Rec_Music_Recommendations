from Database import Database
import hashlib
'''
--- Конвертер из обычных (Влада) в ебанутые(мои в бд)
--- Из таблицы music вытащить все айдишники и преобразовать в обычные (Влада)
'''

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

    def convertAllHistory(self) -> tuple:
        self.__db.clearTable('convhistory')
        tupleDB = self.__db.getAllRecordsTable('history')
        result = []
        for val in tupleDB:
            result.append(self.__string_to_fixed_int(val, 0))
        return result

    def convertAllMusicId(self) -> tuple:
        self.__db.clearTable('convallid')
        tupleDB = self.__db.getAllRecordsTable('music')
        result = []
        for val in tupleDB:
            result.append(self.__string_to_fixed_int(val, 1))
        return result

    def __string_to_fixed_int(self, val, i):
          
        hash_value1 = hashlib.sha256(val[0].encode()).hexdigest()
        fixed_int1 = int(hash_value1[:10], 16) % (10**10)
        fixed_int2 = 0    

        if i == 0:
            hash_value2 = hashlib.sha256(val[1].encode()).hexdigest()
            fixed_int2 = int(hash_value2[:10], 16) % (10**10)
            self.__db.insertDataInConvHistory((fixed_int1, val[0], fixed_int2, val[1]))
        else:
            self.__db.insertDataInConvAllId((fixed_int1, val[0]))
        return (fixed_int1, fixed_int2)

