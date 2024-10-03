from .write_in_files import write_instance_to_example_files, write_instance_to_predict_files
from .TrainingInstance import TrainingInstance
from .PredictInstance import PredictInstance
from termcolor import colored
import tensorflow as tf
from vocab import Vocab
import multiprocessing
import collections
import random
import time

MaskedLmInstance = collections.namedtuple("MaskedLmInstance", ["index", "label"])



def create_masked_lm_predictions(tokens, masked_lm_prob, max_predictions_per_seq, vocab_words, rng, mask_prob):
    """Creates the predictions for the masked LM objective."""

    cand_indexes = []
    for (i, token) in enumerate(tokens):
        if token not in vocab_words:
            continue
        cand_indexes.append(i)

    rng.shuffle(cand_indexes)

    output_tokens = list(tokens)

    num_to_predict = min(max_predictions_per_seq, max(1, int(round(len(tokens) * masked_lm_prob))))

    masked_lms = []
    covered_indexes = set()
    for index in cand_indexes:
        if len(masked_lms) >= num_to_predict:
            break
        if index in covered_indexes:
            continue
        covered_indexes.add(index)

        masked_token = None
        # 80% of the time, replace with [MASK]
        if rng.random() < mask_prob:
            masked_token = "[MASK]"
        else:
            # 10% of the time, keep original
            if rng.random() < 0.5:
                masked_token = tokens[index]
            # 10% of the time, replace with random word
            else:
                # masked_token = vocab_words[rng.randint(0, len(vocab_words) - 1)]
                masked_token = rng.choice(vocab_words)

        output_tokens[index] = masked_token

        masked_lms.append(MaskedLmInstance(index=index, label=tokens[index]))

    masked_lms = sorted(masked_lms, key=lambda x: x.index)

    masked_lm_positions = []
    masked_lm_labels = []
    for p in masked_lms:
        masked_lm_positions.append(p.index)
        masked_lm_labels.append(p.label)

    return (output_tokens, masked_lm_positions, masked_lm_labels)


def create_instances_from_document_train(all_documents, user, max_seq_length, masked_lm_prob, max_predictions_per_seq, vocab, rng, mask_prob):
    """Creates `TrainingInstance`s for a single document."""
    document = all_documents[user]

    max_num_tokens = max_seq_length

    instances = []
    info = [int(user.split("_")[1])]
    vocab_items = vocab.get_items

    for tokens in document:
        assert len(tokens) >= 1 and len(tokens) <= max_num_tokens

        (tokens, masked_lm_positions, masked_lm_labels) = create_masked_lm_predictions(tokens, masked_lm_prob, max_predictions_per_seq, 
                                                                                       vocab_items, rng, mask_prob)

        instance = TrainingInstance(
            info=info,
            tokens=tokens,
            masked_lm_positions=masked_lm_positions,
            masked_lm_labels=masked_lm_labels)
        instances.append(instance)

    return instances


def create_instances_threading(all_documents, max_seq_length, masked_lm_prob, max_predictions_per_seq, vocab, rng, mask_prob, step):
    cnt = 0
    start_time = time.time()
    instances = []
    for user in all_documents:
        cnt += 1
        if cnt % 1000 == 0:
            name = multiprocessing.current_process().name
            time_in_str = time.time() - start_time
            print(f"step: {step}, name: {name}, step: {cnt}, time: {time_in_str:.2f}")
            start_time = time.time()

        instance = create_instances_from_document_train(all_documents, user, max_seq_length, masked_lm_prob, 
                                                        max_predictions_per_seq, vocab, rng, mask_prob)

        instances.extend(instance)

    return instances


def create_training_instances(all_documents_raw, max_seq_length, masked_lm_prob, mask_prob, max_predictions_per_seq, vocab, rng, dupe_factor, prop_sliding_window, pool_size, force_last=False):
    """
    
        Create `TrainingInstance`s from raw text.

        Создайте "Обучающий экземпляр" из необработанного текста.
    
    """
    start_time = time.time()

    all_documents = {}

    if force_last:
        max_num_tokens = max_seq_length
        for user, item_seq in all_documents_raw.items():
            if len(item_seq) == 0:
                print(colored(f"Получили пустую последовательность у пользователя: {user}", 'red', attrs=['underline']))
                continue
            all_documents[user] = [item_seq[-max_num_tokens:]]   
    else:
        max_num_tokens = max_seq_length  # we need two sentence

        sliding_step = (int)(prop_sliding_window * max_num_tokens) if prop_sliding_window != -1.0 else max_num_tokens
        for user, item_seq in all_documents_raw.items():

            if len(item_seq) == 0:
                print(colored(f"Получили пустую последовательность у пользователя: {user}", 'red', attrs=['underline']))
                continue

            if(len(item_seq) > max_num_tokens): # Делим item_seq на 3 равных max_num_tokens массива (они пересекаются)
                difference = len(item_seq) - max_num_tokens
                beg_idx = list(range(difference, 0, -sliding_step))
                beg_idx.append(0)
                beg_idx = beg_idx[::-1]
                all_documents[user] = [item_seq[i:i + max_num_tokens] for i in beg_idx]
                continue

            all_documents[user] = [item_seq]

    instances = []

    print(colored(f"Количество пользователей (документов): {len(all_documents)}", attrs=['bold']))

    if force_last:
        for user in all_documents: # Цикл создает "Обучающий экземпляр" для каждого пользователя
            train_instance = create_instances_from_document_test(all_documents, user, max_seq_length)
            instances.extend(train_instance)
    else:

        pool = multiprocessing.Pool(processes=pool_size)    

        def log_result(result):
            print("callback function result type: {}, size: {} ".format(type(result), len(result)))
            instances.extend(result)

        def error_call(error):
            print(f'ERROR {error}')
            
        for step in range(dupe_factor):

            random_seed = random.randint(1, 10000)

            args = (all_documents, max_seq_length, masked_lm_prob, max_predictions_per_seq, 
                    vocab, random.Random(random_seed), mask_prob, step)

            pool.apply_async(create_instances_threading, args=args, callback=log_result, error_callback=error_call)
        
        pool.close()
        pool.join()

        for user in all_documents: # Цикл создает "Обучающий экземпляр" для каждого пользователя
            train_instance = mask_last(all_documents, user, max_seq_length)
            instances.extend(train_instance)

    end_time = time.time()

    print(colored(f"Количество экземпляров:{len(instances)}; Потрачено времени:{end_time - start_time:.2f} секунд", attrs=['bold']))

    rng.shuffle(instances)
    return instances


def mask_last(all_documents, user, max_seq_length):
    """
        Creates `TrainingInstance`s for a single document.
        
        Создает "Обучающий экземпляр" для одного документа.
    """
    document = all_documents[user] # Берем набор данных по одному пользователю  
    max_num_tokens = max_seq_length
    
    instances = []
    info = [int(user.split("_")[1])] # Берем чиленный id пользователя 

    for tokens in document:
        assert len(tokens) >= 1 and len(tokens) <= max_num_tokens
        
        (tokens, masked_lm_positions, masked_lm_labels) = create_masked_lm_predictions_force_last(tokens)

        instance = TrainingInstance(
            info=info,
            tokens=tokens,
            masked_lm_positions=masked_lm_positions,
            masked_lm_labels=masked_lm_labels)
        
        instances.append(instance)

    return instances


def create_instances_from_document_test(all_documents, user, max_seq_length):
    """
    
        Creates `TrainingInstance`s for a single document.
    
        Создает "Обучающий экземпляр" для одного документа.

        Берутся токены только первой последовательности

    """
    document = all_documents[user]
    max_num_tokens = max_seq_length
    
    assert len(document) == 1 and len(document[0]) <= max_num_tokens
    
    tokens = document[0]

    assert len(tokens) >= 1

    (tokens, masked_lm_positions, masked_lm_labels) = create_masked_lm_predictions_force_last(tokens)

    info = [int(user.split("_")[1])]
    instance = TrainingInstance(
        info=info,
        tokens=tokens,
        masked_lm_positions=masked_lm_positions,
        masked_lm_labels=masked_lm_labels)

    return [instance]


def create_masked_lm_predictions_force_last(tokens):
    """
        Creates the predictions for the masked LM objective.
    
        Создает прогнозы для замаскированной цели LM. (Learning Machine)

        (Маскирует последний элемент последовательности [MASK])
    """

    last_index = -1
    for (i, token) in enumerate(tokens):
        if token == "[CLS]" or token == "[PAD]" or token == '[NO_USE]':
            continue
        last_index = i

    assert last_index > 0

    output_tokens = list(tokens)
    output_tokens[last_index] = "[MASK]"

    masked_lm_positions = [last_index]
    masked_lm_labels = [tokens[last_index]]

    return (output_tokens, masked_lm_positions, masked_lm_labels)


def gen_samples(data, output_filename, rng, dupe_factor, vocab, max_seq_length, max_predictions_per_seq, masked_lm_prob, mask_prob, prop_sliding_window, pool_size, force_last=False):
    '''
    
        Создает "Обучающий экземпляр" или "Тестовые данные" (работает от force_last) 
        для последовательности каждого пользователя и сохраняет результаты в 
        'название папки с данными'/'название файла'.train.tfrecord или 'название папки с данными'/'название файла'.test.tfrecord

    '''
    
    # Начало тренировки
    instances = create_training_instances(data, max_seq_length, masked_lm_prob, mask_prob, max_predictions_per_seq, vocab, rng, dupe_factor, prop_sliding_window, pool_size, force_last)

    tf.compat.v1.logging.info("*** Writing to output files ***")
    tf.compat.v1.logging.info("  %s", output_filename)

    # Запись экземпляров в файл
    write_instance_to_example_files(instances, max_seq_length, max_predictions_per_seq, vocab, [output_filename])


def generate_train_file(user_train_data, output_filename, rng, dupe_factor, vocab, max_seq_length, max_predictions_per_seq, masked_lm_prob, mask_prob, prop_sliding_window, pool_size)->None:
    print(colored('Начало генерации тренировочных данных', 'yellow', attrs=['bold']))
    gen_samples(user_train_data, output_filename, 
                rng, dupe_factor, vocab,  
                max_seq_length, max_predictions_per_seq, masked_lm_prob, mask_prob,
                prop_sliding_window, pool_size, force_last=False)
    print(colored(f'Файл с тренировочными данными: {output_filename}', 'green', attrs=['underline']))


def generate_test_file(user_test_data, output_filename, rng, vocab, max_seq_length, max_predictions_per_seq)->None:
    print(colored('Начало генерации тестовых данных', 'yellow', attrs=['bold']))
    gen_samples(user_test_data, output_filename, 
                rng, None, vocab, 
                max_seq_length, max_predictions_per_seq, None, None,
                None, None, force_last=True)
    print(colored(f'Файл с тестовыми данными: {output_filename}', 'green', attrs=['underline']))


def create_predict_instance(user_hist_data, output_filename, vocab, max_seq_length):
    user = list(user_hist_data.keys())[0]

    tokens = user_hist_data[user]
    
    assert len(tokens) >= 1

    tokens.append('[MASK]')
    masked_lm_positions = len(tokens) - 1

    info = [int(user.split("_")[1])]
    instance = PredictInstance(
        info=info,
        tokens=tokens,
        masked_lm_positions=[masked_lm_positions])
    
    return instance


def gen_predict_samples(user_hist_data, output_filename, vocab, max_seq_length, max_predictions_per_seq):
    '''
    
        Создает "Экземпляр для прогнозирования" для последовательности пользователя и сохраняет результаты в 
        'название папки с данными'/'название файла'.predict.tfrecord

    '''
    instance = create_predict_instance(user_hist_data, output_filename, vocab, max_seq_length)

    tf.compat.v1.logging.info("*** Writing to output files ***")
    tf.compat.v1.logging.info("  %s", output_filename)

    write_instance_to_predict_files(instance, output_filename, vocab, max_seq_length, max_predictions_per_seq)


def generate_predict_file(user_hist_data, output_filename, vocab, max_seq_length, max_predictions_per_seq)->None:
    print(colored('Начало генерации файлы с данными истории пользователя', 'yellow', attrs=['bold']))
    gen_predict_samples(user_hist_data, output_filename, vocab, max_seq_length, max_predictions_per_seq)
    print(colored(f'Файл с данными истории пользователя: {output_filename}', 'green', attrs=['underline']))