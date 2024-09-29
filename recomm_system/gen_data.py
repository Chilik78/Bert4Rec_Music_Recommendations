from generate_data.write_in_files import write_other_files
from generate_data.generate_data import generate_test_files, generate_train_files
from termcolor import colored
import os
import random
import tensorflow as tf
from util import *
from vocab.Vocab import Vocab
import time

PARAMETERS = {
    "output_dir": './data/ml-1m/', # Путь папке с данными
    "dataset_name": 'ml-1m', # Название датасета
    "version_id": '', # ID версии
    "random_seed": 12345,
    "dupe_factor": 10, # Кол-во клонирования данных пользователей
    "max_seq_length": 128, # Максимальная длина последовательности
    "max_predictions_per_seq": 20, # Максимальное кол-во прогнозов в последовательности
    "prop_sliding_window": 0.1, # Размер шага скользящего окна (для работы с массивами)
    "pool_size": 10, # Количество процессов для асинхронной генерации тренировочных данных (ускоряет процесс генерации данных)
    "masked_lm_prob": 0.2, # Процент последовательности, который нужно замаскировать (для тренировочных данных)
    "mask_prob": 1.0 # Вероятность замаскировать элемент последовательности (для тренировочных данных)
}




def show_info_dataset(user_train, user_valid, user_test, usernum, itemnum)->None:
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


def get_train_data(train_data)->dict:
    return {
        f'user_{str(user_id)}': [f'item_{str(item_id)}' for item_id in v]
        for user_id, v in train_data.items() if len(v) > 0
    }


def get_test_data(train_data, test_data)->dict:
    return {
        f'user_{str(user_id)}': [f'item_{str(item_id)}' for item_id in (train_data[user_id] + test_data[user_id])]
        for user_id in train_data if len(train_data[user_id]) > 0 and len(test_data[user_id]) > 0
    }


def get_test_data_output(vocab:Vocab, user_test_data)->dict:
    '''Создание данных, где ключ - id пользователя, а значение - id токенов из словаря (vocab)'''
    user_test_data_output = {k: [vocab.convert_tokens_to_ids(v)] for k, v in user_test_data.items()}
    return user_test_data_output


def show_info_vocab(vocab:Vocab)->None:
    vocab_size_in_str = f"vocab_size:{vocab.get_vocab_size}"
    user_size_in_str = f"user_size:{vocab.get_user_count}"
    item_size_in_str = f"item_size:{vocab.get_item_count}"
    item_with_other_size_int_str = f"item_with_other_size:{vocab.get_item_count + vocab.get_special_token_count}"
    print(colored(f'{vocab_size_in_str}, {user_size_in_str}, {item_size_in_str}, {item_with_other_size_int_str}', 'blue', attrs=['underline']))


def main():

    start_time = time.time()

    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.DEBUG) # Установка вывода логов в консоль от tensorflow
    
    output_dir = PARAMETERS['output_dir'] # Путь папке с данными
    dataset_name = PARAMETERS['dataset_name'] # Название датасета
    version_id = PARAMETERS['version_id'] # ID версии

    dupe_factor = PARAMETERS['dupe_factor'] # Кол-во клонирования данных пользователей
    random_seed = PARAMETERS['random_seed']
    max_seq_length = PARAMETERS['max_seq_length'] # Максимальная длина последовательности
    max_predictions_per_seq = PARAMETERS['max_predictions_per_seq'] # Максимальное кол-во прогнозов в последовательности
    prop_sliding_window = PARAMETERS['prop_sliding_window'] # Размер шага скользящего окна (для работы с массивами)
    pool_size = PARAMETERS['pool_size'] # Количество процессов для асинхронной генерации тренировочных данных (ускоряет процесс генерации данных)
    masked_lm_prob = PARAMETERS['masked_lm_prob'] # Процент последовательности, который нужно замаскировать (для тренировочных данных)
    mask_prob = PARAMETERS['mask_prob'] # Вероятность замаскировать элемент последовательности (для тренировочных данных)
    

    if not os.path.isdir(output_dir):
        print(output_dir + ' is not exist')
        print(os.getcwd())
        exit(1)

    dataset = data_partition(output_dir+dataset_name+'.txt')

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

    show_info_dataset(user_train, user_valid, user_test, usernum, itemnum)

    user_train_data = get_train_data(user_train)
    user_test_data = get_test_data(user_train, user_test)

    vocab = Vocab(user_test_data)
    user_test_data_output = get_test_data_output(vocab, user_test_data)

    rng = random.Random(random_seed)

    output_filename = output_dir + dataset_name + version_id + '.train.tfrecord'
    generate_train_files(user_train_data, output_filename, rng, dupe_factor, vocab, max_seq_length, max_predictions_per_seq, masked_lm_prob, mask_prob, prop_sliding_window, pool_size)

    output_filename = output_dir + dataset_name + version_id + '.test.tfrecord'
    generate_test_files(user_test_data, output_filename, rng, vocab, max_seq_length, max_predictions_per_seq)

    show_info_vocab(vocab)
    
    vocab_file_name = output_dir + dataset_name + version_id + '.vocab'
    write_other_files(vocab, f'Vocab pickle файл: {vocab_file_name}', vocab_file_name)

    his_file_name = output_dir + dataset_name + version_id + '.his'
    write_other_files(user_test_data_output, f'Test data pickle файл: {his_file_name}', his_file_name)

    end_time = time.time()
    print(colored(f'Готово за {end_time - start_time:.2f} секунд', 'green', attrs=['bold']))


if __name__ == "__main__":
    main()