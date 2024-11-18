from api.recommendation_system.generate_data.generate_data import generate_test_file, generate_train_file, generate_predict_file
from api.recommendation_system.generate_data.write_in_files import write_other_files
from collections import defaultdict
from api.recommendation_system.vocab.Vocab import Vocab
from termcolor import colored
import tensorflow as tf
import random
import time
import os

class GeneratorData:
    '''
        Класс GeneratorData используется для генерации файлов для модели

        Основное применение - генерация файлов для модели

        Приватные поля
        --------------

        `output_dir` - Путь папке с данными

        `dataset_name` - Название датасета

        `version_id` - ID версии

        `dupe_factor` - Кол-во клонирования данных пользователей

        `random_seed` - Seed для рандома

        `max_seq_length` - Максимальная длина последовательности

        `prop_sliding_window` - Размер шага скользящего окна (для работы с массивами)

        `pool_size` - Количество процессов для асинхронной генерации тренировочных данных (ускоряет процесс генерации данных)

        `masked_lm_prob` - Процент последовательности, который нужно замаскировать (для тренировочных данных)

        `mask_prob` - Вероятность замаскировать элемент последовательности (для тренировочных данных)

        Методы
        ------

        `set_logging` - Изменение состояния логирования

        `gen_files_for_train` - Генерирует файлы для обучения и оценки модели

        `gen_file_for_predict` - Генерирует файлы для прогнозирования модели
    '''

    def __init__(self, 
                 output_dir:str='./data/music/', 
                 dataset_name:str='music', 
                 version_id:str='', 
                 dupe_factor:int=10, 
                 random_seed:int=12345, 
                 max_seq_length:int=128, 
                 max_predictions_per_seq:int=20,
                 prop_sliding_window:float=0.1,
                 pool_size:int=10,
                 masked_lm_prob:float=0.2, 
                 mask_prob:float=1.0,
                 use_logging:bool=False
                 ) -> None:
        
        '''

            Конструктор генератора файлов для модели

            Параметры
            ---------

            `output_dir` - Путь папке с данными

            `dataset_name` - Название датасета

            `version_id` - ID версии

            `dupe_factor` - Кол-во клонирования данных пользователей

            `random_seed` - Seed для рандома

            `max_seq_length` - Максимальная длина последовательности

            `prop_sliding_window` - Размер шага скользящего окна (для работы с массивами)

            `pool_size` - Количество процессов для асинхронной генерации тренировочных данных (ускоряет процесс генерации данных)

            `masked_lm_prob` - Процент последовательности, который нужно замаскировать (для тренировочных данных)

            `mask_prob` - Вероятность замаскировать элемент последовательности (для тренировочных данных)

        '''


        self.__output_dir = output_dir # Путь папке с данными
        self.__dataset_name = dataset_name # Название датасета
        self.__version_id = version_id # ID версии

        self.__dupe_factor = dupe_factor # Кол-во клонирования данных пользователей
        self.__random_seed = random_seed # Seed для рандома
        self.__max_seq_length = max_seq_length # Максимальная длина последовательности
        self.__max_predictions_per_seq = max_predictions_per_seq # Максимальное кол-во прогнозов в последовательности
        self.__prop_sliding_window = prop_sliding_window # Размер шага скользящего окна (для работы с массивами)
        self.__pool_size = pool_size # Количество процессов для асинхронной генерации тренировочных данных (ускоряет процесс генерации данных)
        self.__masked_lm_prob = masked_lm_prob # Процент последовательности, который нужно замаскировать (для тренировочных данных)
        self.__mask_prob = mask_prob # Вероятность замаскировать элемент последовательности (для тренировочных данных)

        self.set_logging(use_logging)

    
    def set_logging(self, logging:bool):
        '''
        Измененяет состояния логирования

        Параметры
        ---------

        `logging` - новое состояние логирования

        '''
        self.__is_logging=logging

        tf_logging_mode = tf.compat.v1.logging.INFO if self.__is_logging else tf.compat.v1.logging.FATAL
        tf.compat.v1.logging.set_verbosity(tf_logging_mode) # Установка вывода логов в консоль от tensorflow


    def gen_files_for_train(self)->None:
        '''Генерирует файлы для обучения и оценки модели'''

        start_time = time.time()
        
        if not os.path.isdir(self.__output_dir):
            print(self.__output_dir + ' is not exist')
            print(os.getcwd())
            exit(1)

        dataset = self.__data_partition(self.__output_dir+self.__dataset_name+'.txt')

        # User Train - содержит последовательности всех пользователей, только последние два элемента полседовательности стираются
        # User Valid - содержит только предпоследний элемент полседовательности всех пользователей
        # User Train - содержит только последний элемент полседовательности всех пользователей
        # Usernum - последний id пользователя
        # Itemnum - кол-во элементов всех пользователей
        [user_train, user_valid, user_test, usernum, itemnum] = dataset 
        

        # Запуск проверки подлинности в тренировке (Непонятно зачем нужен этот цикл)
        for u in user_train:
            if u in user_valid: # Это странно работает O_o
                user_train[u].extend(user_valid[u])

        if(self.__is_logging):
            self.__show_info_dataset(user_train, user_valid, user_test, usernum, itemnum)

        user_train_data = self.__get_train_data(user_train)
        user_test_data = self.__get_test_data(user_train, user_test)
    
        vocab = Vocab(user_test_data)
        user_test_data_output = self.__get_test_data_output(vocab, user_test_data)

        rng = random.Random(self.__random_seed)

        filename = self.__output_dir + self.__dataset_name + self.__version_id

        output_filename = filename + '.train.tfrecord'
        generate_train_file(user_train_data, output_filename, rng, self.__dupe_factor, vocab, 
                            self.__max_seq_length, self.__max_predictions_per_seq, self.__masked_lm_prob, 
                            self.__mask_prob, self.__prop_sliding_window, self.__pool_size, self.__is_logging)

        output_filename = filename + '.test.tfrecord'
        generate_test_file(user_test_data, output_filename, rng, vocab, self.__max_seq_length, self.__max_predictions_per_seq, self.__is_logging)

        if(self.__is_logging):
            self.__show_info_vocab(vocab)
        
        vocab_file_name = filename + '.vocab'
        write_other_files(vocab, f'Vocab pickle файл: {vocab_file_name}', vocab_file_name, self.__is_logging)

        his_file_name = filename + '.his'
        write_other_files(user_test_data_output, f'Test data pickle файл: {his_file_name}', his_file_name, self.__is_logging)

        end_time = time.time()
        if(self.__is_logging):
            print(colored(f'Готово за {end_time - start_time:.2f} секунд', 'green', attrs=['bold']))


    def gen_file_for_predict(self):
        '''Генерирует файлы для прогнозирования модели'''

        start_time = time.time()

        if not os.path.isdir(self.__output_dir):
            print(self.__output_dir + ' is not exist')
            print(os.getcwd())
            exit(1)

        dataset = self.__data_partition(self.__output_dir+self.__dataset_name+'.txt')

        # User Train - содержит последовательности всех пользователей, только последние два элемента полседовательности стираются
        # User Valid - содержит только предпоследний элемент полседовательности всех пользователей
        # User Train - содержит только последний элемент полседовательности всех пользователей
        # Usernum - последний id пользователя
        # Itemnum - кол-во элементов всех пользователей
        [user_train, user_valid, user_test, usernum, itemnum] = dataset 
        user_history = self.__read_data(self.__output_dir+'user_history.txt')

        # Запуск проверки подлинности в тренировке (Непонятно зачем нужен этот цикл)
        for u in user_train:
            if u in user_valid: # Это странно работает O_o
                user_train[u].extend(user_valid[u])

        if(self.__is_logging):
            self.__show_info_dataset(user_train, user_valid, user_test, usernum, itemnum)

        user_test_data = self.__get_test_data(user_train, user_test)
        user_history_data = self.__get_his_data(user_history)

        vocab = Vocab(user_test_data)

        output_filename = self.__output_dir + self.__dataset_name + self.__version_id + '.predict.tfrecord'
        generate_predict_file(user_history_data, output_filename, vocab, self.__max_seq_length, self.__max_predictions_per_seq, self.__is_logging)

        end_time = time.time()
        if(self.__is_logging):
            print(colored(f'Готово за {end_time - start_time:.2f} секунд', 'green', attrs=['bold']))


    def __data_partition(self, fname)->list:
        usernum = 0
        itemnum = 0
        User = defaultdict(list)
        user_train = {}
        user_valid = {}
        user_test = {}
        # assume user/item index starting from 1
        f = open(fname, 'r')
        for line in f:
            u, i = line.rstrip().split(' ')
            u = int(u)
            i = int(i)
            usernum = max(u, usernum)
            itemnum = max(i, itemnum)
            User[u].append(i)

        f.close()

        for user in User:
            nfeedback = len(User[user])
            if nfeedback < 3:
                user_train[user] = User[user]
                user_valid[user] = []
                user_test[user] = []
            else:
                user_train[user] = User[user][:-2]
                user_valid[user] = []
                user_valid[user].append(User[user][-2])
                user_test[user] = []
                user_test[user].append(User[user][-1])
        
        return [user_train, user_valid, user_test, usernum, itemnum]


    def __read_data(self, fname)->dict:
        user_data = defaultdict(list)

        f = open(fname, 'r')
        for line in f:
            u, i = line.rstrip().split(' ')
            u = int(u)
            i = int(i)
            user_data[u].append(i)
            
        f.close()

        return dict(user_data)


    def __show_info_dataset(self, user_train, user_valid, user_test, usernum, itemnum)->None:
        cc = 0.0
        max_len = 0
        min_len = 100000
        for u in user_train:
            cc += len(user_train[u])
            max_len = max(len(user_train[u]), max_len)
            min_len = min(len(user_train[u]), min_len)
        print(colored(f'Средняя длина последовательности: {(cc / len(user_train)):.2f}', attrs=['underline']))
        print(colored(f'max:{max_len}, min:{min_len}', attrs=['underline']))
        print(colored(f'len_train:{len(user_train)}, len_valid:{len(user_valid)}, len_test:{len(user_test)}, usernum:{usernum}, itemnum:{itemnum}', "blue", attrs=['underline']))


    def __get_train_data(self, train_data)->dict:
        return {
            f'user_{str(user_id)}': [f'item_{str(item_id)}' for item_id in v]
            for user_id, v in train_data.items() if len(v) > 0
        }


    def __get_test_data(self, train_data, test_data)->dict:
        return {
            f'user_{str(user_id)}': [f'item_{str(item_id)}' for item_id in (train_data[user_id] + test_data[user_id])]
            for user_id in train_data if len(train_data[user_id]) > 0 and len(test_data[user_id]) > 0
        }
    

    def __get_his_data(self, history_data)->dict:
        return {
            f'user_{str(user_id)}': [f'item_{str(item_id)}' for item_id in v]
            for user_id, v in history_data.items() if len(v) > 0
        }


    def __get_test_data_output(self, vocab:Vocab, user_test_data)->dict:
        '''Создание данных, где ключ - id пользователя, а значение - id токенов из словаря (vocab)'''
        user_test_data_output = {k: [vocab.convert_tokens_to_ids(v)] for k, v in user_test_data.items()}
        return user_test_data_output
    

    def __show_info_vocab(self, vocab:Vocab)->None:
        vocab_size_in_str = f"vocab_size:{vocab.get_vocab_size}"
        user_size_in_str = f"user_size:{vocab.get_user_count}"
        item_size_in_str = f"item_size:{vocab.get_item_count}"
        item_with_other_size_int_str = f"item_with_other_size:{vocab.get_item_count + vocab.get_special_token_count}"
        print(colored(f'{vocab_size_in_str}, {user_size_in_str}, {item_size_in_str}, {item_with_other_size_int_str}', 'blue', attrs=['underline']))



if __name__ == "__main__":
    gd = GeneratorData(use_logging=True)
    gd.gen_files_for_train()