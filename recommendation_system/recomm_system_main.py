from model.modeling.support_funcs import get_assignment_map_from_checkpoint
from model.modeling.BertConfig import BertConfig
from model.modeling.BertModel import BertModel
from recomm_system.support_funcs import *
from model.optimization import *
from termcolor import colored
from vocab.Vocab import Vocab
import tensorflow as tf
import numpy as np
import pickle
import time
import sys
import os



# bert_config_file = 'data/steam/bert_config_steam_64.json' # Файл конфигурации гиперпараметров модели
# checkpoint_dir = os.path.normpath('/models/steam') # Файл для сохранения прогресса при тренировке модели
# train_input_file = 'data/steam/steam.train.tfrecord' # Файл с тренировочными данными
# test_input_file = 'data/steam/steam.test.tfrecord' # Файл с тестовыми данными
# predict_input_file = 'data/steam/steam.predict.tfrecord'
# vocab_filename = 'data/steam/steam.vocab' # Файл словаря
# user_history_filename = 'data/steam/steam.his'
# save_checkpoints_steps = 1000 # Через сколько шагов делать чекпоинт
# init_checkpoint = None
# learning_rate = 1e-4
# num_train_steps = 100000 # Кол-во максимальных шагов при тренировке 
# num_warmup_steps = 100
# use_tpu = False
# batch_size = 32
# max_seq_length = 128 # Максимальный размер последовательности
# max_predictions_per_seq = 20 # Максимальное кол-во прогнозов в последовательности
# use_pop_random = True
# mode_recomm_system = "PREDICT" # Режим работы рекомендательной системы (TRAIN, EVAL, PREDICT)


bert_config_file = 'data/ml-1m/bert_config_ml-1m_64.json' # Файл конфигурации гиперпараметров модели
checkpoint_dir = os.path.normpath('/models/ml-1m') # Файл для сохранения прогресса при тренировке модели
train_input_file = 'data/ml-1m/ml-1m.train.tfrecord' # Файл с тренировочными данными
test_input_file = 'data/ml-1m/ml-1m.test.tfrecord' # Файл с тестовыми данными
predict_input_file = 'data/ml-1m/ml-1m.predict.tfrecord'
vocab_filename = 'data/ml-1m/ml-1m.vocab' # Файл словаря
user_history_filename = 'data/ml-1m/ml-1m.his'
save_checkpoints_steps = 1000 # Через сколько шагов делать чекпоинт
init_checkpoint = None
learning_rate = 1e-4
num_train_steps = 100000 # Кол-во максимальных шагов при тренировке 
num_warmup_steps = 100
use_tpu = False
batch_size = 32
max_seq_length = 128 # Максимальный размер последовательности
max_predictions_per_seq = 20 # Максимальное кол-во прогнозов в последовательности 
use_pop_random = True
mode_recomm_system = "PREDICT" # Режим работы рекомендательной системы (TRAIN, EVAL, PREDICT)



def model_fn_builder(bert_config, init_checkpoint, learning_rate, num_train_steps, num_warmup_steps, use_tpu, use_one_hot_embeddings, item_size):
    """Возвращает функцию `model_fn` для Estimator."""

    def model_fn(features, labels, mode, params):
        """Возвращает функция `model_fn` для Estimator."""

        print("*** Features ***")
        for name in sorted(features.keys()):
            print(f"  name = {name}, shape = {features[name].shape}")

        info = features["info"]
        input_ids = features["input_ids"]
        input_mask = features["input_mask"]
        masked_lm_positions = features["masked_lm_positions"]
        masked_lm_ids = features["masked_lm_ids"]
        masked_lm_weights = features["masked_lm_weights"]

        is_training = (mode == tf.estimator.ModeKeys.TRAIN)

        model = BertModel(
            config=bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=None,
            use_one_hot_embeddings=use_one_hot_embeddings)

        sequence_output = model.get_sequence_output()
        embedding_table = model.get_embedding_table()

        (masked_lm_loss, masked_lm_example_loss, masked_lm_log_probs) = get_masked_lm_output(bert_config, sequence_output, embedding_table, 
                                                                                             masked_lm_positions, masked_lm_ids, masked_lm_weights)

        total_loss = masked_lm_loss

        tvars = tf.compat.v1.trainable_variables()

        initialized_variable_names = {}
        scaffold_fn = None
        if init_checkpoint:
            (assignment_map, initialized_variable_names) = get_assignment_map_from_checkpoint(tvars, init_checkpoint)
            if use_tpu: 
                tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)
                scaffold_fn = tf.compat.v1.train.Scaffold()
            else:
                tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)

        print("**** Trainable Variables ****")
        for var in tvars:
            init_string = ""
            if var.name in initialized_variable_names:
                init_string = ", *INIT_FROM_CKPT*"
            print(f"  name = {var.name}, shape = {var.shape}{init_string}")

        if mode == tf.estimator.ModeKeys.TRAIN:
            train_op = create_optimizer(total_loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu)

            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=total_loss,
                train_op=train_op,
                scaffold=scaffold_fn)
            
        elif mode == tf.estimator.ModeKeys.EVAL:

            tf.compat.v1.add_to_collection('eval_sp', masked_lm_log_probs)
            tf.compat.v1.add_to_collection('eval_sp', input_ids)
            tf.compat.v1.add_to_collection('eval_sp', masked_lm_ids)
            tf.compat.v1.add_to_collection('eval_sp', info)

            eval_metrics = metric_fn(masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids, masked_lm_weights)
            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=total_loss,
                eval_metric_ops=eval_metrics,
                scaffold=scaffold_fn)
            
        elif mode == tf.estimator.ModeKeys.PREDICT:
            seq_pred = get_predictions(masked_lm_log_probs)

            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=seq_pred)

        return output_spec

    return model_fn


def input_fn_builder(input_files, max_seq_length, max_predictions_per_seq, is_training, num_cpu_threads=4):
    """Возвращает функцию `input_fn` для Estimator"""

    def input_fn(params):
        """Фактическая функция ввода"""
        batch_size = params["batch_size"]

        name_to_features = {
            "info": tf.compat.v1.FixedLenFeature([1], tf.int64),  # [user]
            "input_ids": tf.compat.v1.FixedLenFeature([max_seq_length], tf.int64, default_value=[0] * max_seq_length),
            "input_mask": tf.compat.v1.FixedLenFeature([max_seq_length], tf.int64, default_value=[0] * max_seq_length),
            "masked_lm_positions": tf.compat.v1.FixedLenFeature([max_predictions_per_seq], tf.int64, default_value=[0] * max_predictions_per_seq),
            "masked_lm_ids": tf.compat.v1.FixedLenFeature([max_predictions_per_seq], tf.int64),
            "masked_lm_weights": tf.compat.v1.FixedLenFeature([max_predictions_per_seq], tf.float32, default_value=[0.0] * max_predictions_per_seq)
        }

        # Для обучения нам нужно много параллельного чтения и перетасовки.
        # Для оценки мы не хотим перетасовки, и параллельное чтение не имеет значения.
        if is_training:
            d = tf.data.TFRecordDataset(input_files)
            d = d.repeat()
            d = d.shuffle(buffer_size=100)

        else:
            d = tf.data.TFRecordDataset(input_files)

        d = d.map(
            lambda record: decode_record(record, name_to_features),
            num_parallel_calls=num_cpu_threads)
        d = d.batch(batch_size=batch_size)
        return d

    return input_fn


class EvalHooks(tf.compat.v1.train.SessionRunHook):
    def __init__(self):
        print('run init EvalHooks')

    def begin(self):
        self.valid_user = 0.0

        self.ndcg_1 = 0.0
        self.hit_1 = 0.0
        self.ndcg_5 = 0.0
        self.hit_5 = 0.0
        self.ndcg_10 = 0.0
        self.hit_10 = 0.0
        self.ap = 0.0

        np.random.seed(12345)

        self.vocab = None

        if user_history_filename is not None:
            print('load user history from :' + user_history_filename)
            with open(user_history_filename, 'rb') as input_file:
                self.user_history = pickle.load(input_file)

        if vocab_filename is not None:
            print('load vocab from :' + vocab_filename)
            with open(vocab_filename, 'rb') as input_file:
                self.vocab = pickle.load(input_file)

            keys = self.vocab.counter.keys()
            values = self.vocab.counter.values()
            self.ids = self.vocab.convert_tokens_to_ids(keys)
            # normalize
            # print(values)
            sum_value = np.sum([x for x in values])
            # print(sum_value)
            self.probability = [value / sum_value for value in values]

    def end(self, session):
        print("ndcg@1:{}, hit@1:{}， ndcg@5:{}, hit@5:{}, ndcg@10:{}, hit@10:{}, ap:{}, valid_user:{}".
            format(self.ndcg_1 / self.valid_user, self.hit_1 / self.valid_user,
                   self.ndcg_5 / self.valid_user, self.hit_5 / self.valid_user,
                   self.ndcg_10 / self.valid_user,
                   self.hit_10 / self.valid_user, self.ap / self.valid_user,
                   self.valid_user))

    def before_run(self, run_context):
        variables = tf.compat.v1.get_collection('eval_sp')
        return tf.compat.v1.train.SessionRunArgs(variables)

    def after_run(self, run_context, run_values):
        masked_lm_log_probs, input_ids, masked_lm_ids, info = run_values.results
        masked_lm_log_probs = masked_lm_log_probs.reshape((-1, max_predictions_per_seq, masked_lm_log_probs.shape[1]))

        for idx in range(len(input_ids)):
            rated = set(input_ids[idx])
            rated.add(0)
            rated.add(masked_lm_ids[idx][0])
            map(lambda x: rated.add(x), self.user_history["user_" + str(info[idx][0])][0])
            item_idx = [masked_lm_ids[idx][0]]
            # here we need more consideration
            masked_lm_log_probs_elem = masked_lm_log_probs[idx, 0]
            size_of_prob = len(self.ids) + 1  # len(masked_lm_log_probs_elem)
            if use_pop_random:
                if self.vocab is not None:
                    while len(item_idx) < 101:
                        sampled_ids = np.random.choice(self.ids, 101, replace=False, p=self.probability)
                        sampled_ids = [x for x in sampled_ids if x not in rated and x not in item_idx]
                        item_idx.extend(sampled_ids[:])
                    item_idx = item_idx[:101]
            else:
                # print("evaluation random -> ")
                for _ in range(100):
                    t = np.random.randint(1, size_of_prob)
                    while t in rated:
                        t = np.random.randint(1, size_of_prob)
                    item_idx.append(t)

            predictions = -masked_lm_log_probs_elem[item_idx]
            rank = predictions.argsort().argsort()[0]

            self.valid_user += 1

            if self.valid_user % 100 == 0:
                print('.', end='')
                sys.stdout.flush()

            if rank < 1:
                self.ndcg_1 += 1
                self.hit_1 += 1
            if rank < 5:
                self.ndcg_5 += 1 / np.log2(rank + 2)
                self.hit_5 += 1
            if rank < 10:
                self.ndcg_10 += 1 / np.log2(rank + 2)
                self.hit_10 += 1

            self.ap += 1.0 / (rank + 1)


def do_train(input_files, estimator):
    print(colored("***** Начало тренировки *****", "magenta", attrs=['bold']))
    print(f"  Batch size = {batch_size}")

    train_input_fn = input_fn_builder(
        input_files=input_files,
        max_seq_length=max_seq_length,
        max_predictions_per_seq=max_predictions_per_seq,
        is_training=True)
    
    start_time = time.time()
    estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)
    end_time = time.time() - start_time
    print(colored(f"Конец тренировки: {end_time:.2f} секунд", "magenta", attrs=['bold']))


def do_eval(input_files, estimator, bert_config):
    print(colored("***** Начало оценки *****", "magenta", attrs=['bold']))
    print(f"  Batch size = {batch_size}")

    eval_input_fn = input_fn_builder(
        input_files=input_files,
        max_seq_length=max_seq_length,
        max_predictions_per_seq=max_predictions_per_seq,
        is_training=False)

    start_time = time.time()
    result = estimator.evaluate(
        input_fn=eval_input_fn,
        steps=None,
        hooks=[EvalHooks()])
    end_time = time.time() - start_time
    print(colored(f"Конец оценки: {end_time:.2f} секунд", "magenta", attrs=['bold']))
    
    output_eval_file = os.path.join(checkpoint_dir, "eval_results.txt")
    with tf.compat.v1.gfile.GFile(output_eval_file, "w") as writer:
        print(colored("***** Результаты оценки *****", "magenta", attrs=['bold']))
        print(colored(bert_config.to_json_string(), "magenta", attrs=['bold']))

        writer.write(bert_config.to_json_string() + '\n')
        for key in sorted(result.keys()):
            print(colored(f"{key} = {str(result[key])}", "magenta", attrs=['bold']))
            writer.write("%s = %s\n" % (key, str(result[key])))


def do_predict(input_files, estimator):
    print(colored("***** Начало прогнозирования *****", "magenta", attrs=['bold']))
    print(f"  Batch size = {batch_size}")

    predict_input_fn = input_fn_builder(
        input_files=input_files,
        max_seq_length=max_seq_length,
        max_predictions_per_seq=max_predictions_per_seq,
        is_training=False)

    start_time = time.time()
    result = estimator.predict(input_fn=predict_input_fn)
    end_time = time.time() - start_time
    print(colored(f"Конец прогнозирования: {end_time:.2f} секунд", "magenta", attrs=['bold']))
    
    vocab = None
    with open(vocab_filename, 'rb') as input_file:
        vocab = pickle.load(input_file)
        
    token = ''
    for i in result:
        token = vocab.convert_ids_to_tokens([i])[0]

    print(colored(f"----------Результаты----------\nToken: {token}\nId Item: {vocab.token_to_ids[token]}", "green", attrs=['bold']))


def run_system(train_input_files, test_input_files, predict_input_files, estimator, bert_config):
    if mode_recomm_system == "TRAIN":
        do_train(train_input_files, estimator)
    elif mode_recomm_system == "EVAL":
        do_eval(test_input_files, estimator, bert_config)
    elif mode_recomm_system == "PREDICT":
        do_predict(predict_input_files, estimator)
    else:
        raise Exception(colored("Неверно указан режим работы системы. Возможные значения: TRAIN, EVAL, PREDICT", "red", attrs=['bold', 'underline']))


def main(_):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.FATAL) # Установка вывода логов в консоль от tensorflow

    bert_config = BertConfig.from_json_file(bert_config_file)

    tf.compat.v1.gfile.MakeDirs(checkpoint_dir)

    train_input_files, test_input_files, predict_input_files = get_input_files([train_input_file, test_input_file, predict_input_file], mode_recomm_system)

    run_config = tf.estimator.RunConfig(model_dir=checkpoint_dir, save_checkpoints_steps=save_checkpoints_steps)

    item_size = get_item_size_from_vocab(vocab_filename)
    
    model_fn = model_fn_builder(
        bert_config=bert_config,
        init_checkpoint=init_checkpoint,
        learning_rate=learning_rate,
        num_train_steps=num_train_steps,
        num_warmup_steps=num_warmup_steps,
        use_tpu=use_tpu,
        use_one_hot_embeddings=use_tpu,
        item_size=item_size)

    # Если TPU недоступен, для CPU или GPU будет восстановлен обычный Estimator
    estimator = tf.estimator.Estimator(
        model_fn=model_fn,
        config=run_config,
        params={
            "batch_size": batch_size
        })
    
    run_system(train_input_files, test_input_files, predict_input_files, estimator, bert_config)
    

if __name__ == "__main__":
    tf.compat.v1.app.run()