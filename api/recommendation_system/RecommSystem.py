from api.recommendation_system.model.modeling.support_funcs import get_assignment_map_from_checkpoint, get_shape_list, get_activation, create_initializer, layer_norm
from api.recommendation_system.model.modeling.BertConfig import BertConfig
from api.recommendation_system.model.modeling.BertModel import BertModel
from api.recommendation_system.recomm_system.EvalHooks import EvalHooks
from api.recommendation_system.model.optimization import *
from termcolor import colored
import tensorflow as tf
import time
import os, sys
import pickle

from api.recommendation_system.vocab import *
from . import vocab

sys.modules['vocab'] = vocab

class RecommSystem:

    '''
        Класс RecommSystem используется для обучения, оценки, прогнозирования модели
    
        Основное применение - обучение модели, получение рещультата прогнозирования

        Note:
            Возможны проблемы при обучении модели,
            в пути проекта не должно быть русских символов

        Приватные поля
        --------------

        
        `bert_config_file` - Файл конфигурации гиперпараметров модели

        `checkpoint_dir` - Файл для сохранения прогресса при тренировке модели

        `train_input_file` - Файл с данными для обучения

        `test_input_file` - Файл с тестовыми данными

        `predict_input_file` - Файл с историей пользователя, для прогнозирования

        `vocab_filename` - Файл словаря

        `user_history_filename` - 

        `save_checkpoints_steps` - Количество шагов, через которые модель будет делать чекпоинт

        `init_checkpoint` - 

        `learning_rate` - 

        `num_train_steps` - Кол-во максимальных шагов при тренировке 

        `num_warmup_steps` - 

        `use_tpu` - Используется TPU

        `batch_size` -

        `max_seq_length` - Максимальный размер последовательности

        `max_predictions_per_seq` - Максимальное кол-во прогнозов в последовательности

        `use_pop_random` - 

        `is_logging` - Используется логирование

        `estimator` - Estimator для работы с моделью

        `bert_config` - Конфигурация для модели

        `train_input_files` - Файлы для обучения
        
        `test_input_files` - Файлы для тестирования
        
        `predict_input_files` - Файлы для прогнозирования

        Методы
        ------

        `set_logging` - Изменение состояния логирования

        `do_train` - Обучение модели рекомендательной системы

        `do_eval` - Оценивание модели рекомендательной системы

        `do_predict` - Прогнозирование модели рекомендательной системы

    '''

    def __init__(self, 
                 bert_config_file:str='data/music/bert_config_music_64.json', 
                 checkpoint_dir:str='models/music',
                 train_input_file:str='data/music/music.train.tfrecord',
                 test_input_file:str='data/music/music.test.tfrecord',
                 predict_input_file:str='data/music/music.predict.tfrecord',
                 vocab_filename:str='data/music/music.vocab',
                 user_history_filename:str='data/music/music.his',
                 save_checkpoints_steps:int=1000,
                 init_checkpoint=None,
                 learning_rate:float=1e-4,
                 num_train_steps:int=100000,
                 num_warmup_steps:int=100,
                 use_tpu:bool=False,
                 batch_size:int=32,
                 max_seq_length:int=128,
                 max_predictions_per_seq:int=20,
                 use_pop_random:bool=True,
                 use_logging:bool=False
                 ) -> None:

        '''

            Конструктор модели рекомендательной системы
        
            Параметры
            ---------

            `bert_config_file` - Файл конфигурации гиперпараметров модели

            `checkpoint_dir` - Файл для сохранения прогресса при тренировке модели

            `train_input_file` - Файл с данными для обучения

            `test_input_file` - Файл с тестовыми данными

            `predict_input_file` - Файл с историей пользователя, для прогнозирования

            `vocab_filename` - Файл словаря

            `save_checkpoints_steps` - Количество шагов, через которые модель будет делать чекпоинт

            `num_train_steps` - Кол-во максимальных шагов при тренировке 

            `use_tpu` - Использовать TPU?

            `max_seq_length` - Максимальный размер последовательности

            `max_predictions_per_seq` - Максимальное кол-во прогнозов в последовательности

            `use_logging` - Использовать логирование?
        
        '''
        
        
        def get_path(path):
            return os.path.normpath(os.path.abspath(__file__).removesuffix('\\recommendation_system\\RecommSystem.py') + '\\' + path)
        
        self.__bert_config_file = get_path(bert_config_file) # Файл конфигурации гиперпараметров модели
        self.__checkpoint_dir = get_path(checkpoint_dir) # Файл для сохранения прогресса при тренировке модели
        self.__train_input_file = get_path(train_input_file) # Файл с тренировочными данными
        self.__test_input_file = get_path(test_input_file) # Файл с тестовыми данными
        self.__vocab_filename = get_path(vocab_filename) # Файл словаря
        self.__predict_input_file = get_path(predict_input_file) # Файл с историей пользователя, для прогнозирования
        self.__save_checkpoints_steps = save_checkpoints_steps # Через сколько шагов делать чекпоинт
        self.__user_history_filename = get_path(user_history_filename)
        self.__init_checkpoint = init_checkpoint
        self.__learning_rate = learning_rate
        self.__num_train_steps = num_train_steps # Кол-во максимальных шагов при тренировке 
        self.__num_warmup_steps = num_warmup_steps
        self.__use_tpu = use_tpu # Использовать TPU
        self.__batch_size = batch_size
        self.__max_seq_length = max_seq_length # Максимальный размер последовательности
        self.__max_predictions_per_seq = max_predictions_per_seq # Максимальное кол-во прогнозов в последовательности 
        self.__use_pop_random = use_pop_random

        self.set_logging(use_logging)
        self.__prepare_recomm_system()


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


    def do_train(self, num_train_steps = None):
        '''Запускает обучение модели'''

        if(self.__is_logging):
            print(colored("***** Начало тренировки *****", "magenta", attrs=['bold']))
            print(f"  Batch size = {self.__batch_size}")

        train_input_fn = self.__input_fn_builder(
            input_files=self.__train_input_files,
            max_seq_length=self.__max_seq_length,
            max_predictions_per_seq=self.__max_predictions_per_seq,
            is_training=True)
        
        start_time = time.time()
        self.__estimator.train(input_fn=train_input_fn, max_steps=num_train_steps if num_train_steps else self.__num_train_steps)
        end_time = time.time() - start_time

        if(self.__is_logging):
            print(colored(f"Конец тренировки: {end_time:.2f} секунд", "magenta", attrs=['bold']))


    def do_eval(self):
        '''Запускает оценивание модели'''

        if(self.__is_logging):
            print(colored("***** Начало оценки *****", "magenta", attrs=['bold']))
            print(f"  Batch size = {self.__batch_size}")

        eval_input_fn = self.__input_fn_builder(
            input_files=self.__test_input_files,
            max_seq_length=self.__max_seq_length,
            max_predictions_per_seq=self.__max_predictions_per_seq,
            is_training=False)

        start_time = time.time()
        result = self.__estimator.evaluate(
            input_fn=eval_input_fn,
            steps=None,
            hooks=[EvalHooks(
                is_logging=self.__is_logging,
                user_history_filename=self.__user_history_filename,
                vocab_filename=self.__vocab_filename,
                max_predictions_per_seq=self.__max_predictions_per_seq,
                use_pop_random=self.__use_pop_random
            )])
        end_time = time.time() - start_time

        if(self.__is_logging):
            print(colored(f"Конец оценки: {end_time:.2f} секунд", "magenta", attrs=['bold']))
        
        output_eval_file = os.path.join(self.__checkpoint_dir, "eval_results.txt")
        with tf.compat.v1.gfile.GFile(output_eval_file, "w") as writer:
            if(self.__is_logging):
                print(colored("***** Результаты оценки *****", "magenta", attrs=['bold']))
                print(colored(self.__bert_config.to_json_string(), "magenta", attrs=['bold']))

            writer.write(self.__bert_config.to_json_string() + '\n')
            for key in sorted(result.keys()):
                if(self.__is_logging):
                    print(colored(f"{key} = {str(result[key])}", "magenta", attrs=['bold']))

                writer.write("%s = %s\n" % (key, str(result[key])))


    def do_predict(self):
        '''
        Запускает прогнозирование модели
        
        Возвращаемое значение
        ---------------------

            music id
        
        '''

        if(self.__is_logging):
            print(colored("***** Начало прогнозирования *****", "magenta", attrs=['bold']))
            print(f"  Batch size = {self.__batch_size}")

        predict_input_fn = self.__input_fn_builder(
            input_files=self.__predict_input_files,
            max_seq_length=self.__max_seq_length,
            max_predictions_per_seq=self.__max_predictions_per_seq,
            is_training=False)

        start_time = time.time()
        result = self.__estimator.predict(input_fn=predict_input_fn)
        end_time = time.time() - start_time

        if(self.__is_logging):
            print(colored(f"Конец прогнозирования: {end_time:.2f} секунд", "magenta", attrs=['bold']))
        
        vocab = None
        with open(self.__vocab_filename, 'rb') as input_file:
            vocab = pickle.load(input_file)
            
        token = ''
        for i in result:
            token = vocab.convert_ids_to_tokens([i])[0]

        if(self.__is_logging):
            print(colored(f"----------Результаты----------\nToken: {token}\nId Item: {vocab.token_to_ids[token]}", "green", attrs=['bold']))

        return token.removeprefix('item_')


    def __input_fn_builder(self, input_files, max_seq_length, max_predictions_per_seq, is_training, num_cpu_threads=4):
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
                lambda record: self.__decode_record(record, name_to_features),
                num_parallel_calls=num_cpu_threads)
            d = d.batch(batch_size=batch_size)
            return d

        return input_fn
    

    def __decode_record(self, record, name_to_features):
        """Декодирует запись в примере TensorFlow."""
        example = tf.compat.v1.parse_single_example(record, name_to_features)

        # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
        # So cast all int64 to int32.
        for name in list(example.keys()):
            t = example[name]
            if t.dtype == tf.int64:
                t = tf.compat.v1.to_int32(t)
            example[name] = t

        return example


    def __prepare_recomm_system(self):
        self.__bert_config = BertConfig.from_json_file(self.__bert_config_file)

        tf.compat.v1.gfile.MakeDirs(self.__checkpoint_dir)

        files_paths = [self.__train_input_file, self.__test_input_file, self.__predict_input_file]

        self.__train_input_files, self.__test_input_files, self.__predict_input_files = self.__get_input_files(files_paths)

        item_size = self.__get_item_size_from_vocab(self.__vocab_filename)

        model_fn = self.__model_fn_builder(
            bert_config=self.__bert_config,
            init_checkpoint=self.__init_checkpoint,
            learning_rate=self.__learning_rate,
            num_train_steps=self.__num_train_steps,
            num_warmup_steps=self.__num_warmup_steps,
            use_tpu=self.__use_tpu,
            use_one_hot_embeddings=self.__use_tpu,
            item_size=item_size)
        
        run_config = tf.estimator.RunConfig(model_dir=self.__checkpoint_dir, save_checkpoints_steps=self.__save_checkpoints_steps)
        
        # Если TPU недоступен, для CPU или GPU будет восстановлен обычный Estimator
        self.__estimator = tf.estimator.Estimator(
            model_fn=model_fn,
            config=run_config,
            params={
                "batch_size": self.__batch_size
            })


    def __get_input_files(self, files_paths:list):

        train_input_file = files_paths[0]
        test_input_file = files_paths[1]
        predict_input_file = files_paths[2]

        train_input_files = self.__get_files_paths(train_input_file)

        if test_input_file is None:
            test_input_files = self.__get_files_paths(train_input_file)
        else:
            test_input_files = self.__get_files_paths(test_input_file)

        predict_input_files = self.__get_files_paths(predict_input_file)

        if(self.__is_logging):
            self.__show_info_files_paths("*** Входные файлы для тренировки ***", train_input_files)
            self.__show_info_files_paths("*** Входные файлы для тестировки ***", test_input_files)
            self.__show_info_files_paths("*** Входные файлы для прогнозирования ***", predict_input_files)

        return (train_input_files, test_input_files, predict_input_files)
    

    def __get_files_paths(self, string_with_files_paths:str):
        files_paths = []
        for input_pattern in string_with_files_paths.split(","):
            files_paths.extend(tf.compat.v1.gfile.Glob(input_pattern))
        return files_paths
    

    def __show_info_files_paths(self, text:str, files_paths:list):
        print(text)
        for input_file in files_paths:
            print("  %s" % input_file)

    
    def __get_item_size_from_vocab(self, vocab_filename:str):
        try:
            with open(vocab_filename, 'rb') as input_file:
                vocab = pickle.load(input_file)
            
            return len(vocab.counter)
        
        except Exception as e:
            print(colored(f"Ошибка при чтении vocab файла: {e}", "red", attrs=['bold', 'underline']))


    def __model_fn_builder(self, bert_config, init_checkpoint, learning_rate, num_train_steps, 
                           num_warmup_steps, use_tpu, use_one_hot_embeddings, item_size):
        """Возвращает функцию `model_fn` для Estimator."""

        def model_fn(features, labels, mode, params):
            """Возвращает функция `model_fn` для Estimator."""


            if(self.__is_logging):
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

            (masked_lm_loss, masked_lm_example_loss, masked_lm_log_probs) = self.__get_masked_lm_output(bert_config, sequence_output, embedding_table, 
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

            if(self.__is_logging):
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

                eval_metrics = self.__metric_fn(masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids, masked_lm_weights)
                output_spec = tf.estimator.EstimatorSpec(
                    mode=mode,
                    loss=total_loss,
                    eval_metric_ops=eval_metrics,
                    scaffold=scaffold_fn)
                
            elif mode == tf.estimator.ModeKeys.PREDICT:
                seq_pred = self.__get_predictions(masked_lm_log_probs)

                output_spec = tf.estimator.EstimatorSpec(
                    mode=mode,
                    predictions=seq_pred)

            return output_spec

        return model_fn
    

    def __get_masked_lm_output(self, bert_config, input_tensor, output_weights, positions, label_ids, label_weights):
        """Get loss and log probs for the masked LM."""
        # [batch_size*label_size, dim]
        input_tensor = self.__gather_indexes(input_tensor, positions)

        with tf.compat.v1.variable_scope("cls/predictions"):
            # We apply one more non-linear transformation before the output layer.
            # This matrix is not used after pre-training.
            with tf.compat.v1.variable_scope("transform"):
                dense_input_tensor = tf.keras.layers.Dense(units=bert_config.hidden_size,
                                                        activation=get_activation(bert_config.hidden_act),
                                                        kernel_initializer=create_initializer(
                                                            bert_config.initializer_range
                                                        ))
                # input_tensor = tf.layers.dense(
                #     input_tensor,
                #     units=bert_config.hidden_size,
                #     activation=modeling.get_activation(bert_config.hidden_act),
                #     kernel_initializer=modeling.create_initializer(
                #         bert_config.initializer_range))
                input_tensor = dense_input_tensor(input_tensor)
                input_tensor = layer_norm(input_tensor)

            # The output weights are the same as the input embeddings, but there is
            # an output-only bias for each token.
            output_bias = tf.compat.v1.get_variable(
                "output_bias",
                shape=[output_weights.shape[0]],
                initializer=tf.zeros_initializer())
            logits = tf.matmul(input_tensor, output_weights, transpose_b=True)
            logits = tf.nn.bias_add(logits, output_bias)
            # logits, (bs*label_size, vocab_size)
            log_probs = tf.nn.log_softmax(logits, -1)

            label_ids = tf.reshape(label_ids, [-1])
            label_weights = tf.reshape(label_weights, [-1])

            one_hot_labels = tf.one_hot(label_ids, depth=output_weights.shape[0], dtype=tf.float32)

            # The `positions` tensor might be zero-padded (if the sequence is too
            # short to have the maximum number of predictions). The `label_weights`
            # tensor has a value of 1.0 for every real prediction and 0.0 for the
            # padding predictions.
            per_example_loss = -tf.reduce_sum(log_probs * one_hot_labels, axis=[-1])
            numerator = tf.reduce_sum(label_weights * per_example_loss)
            denominator = tf.reduce_sum(label_weights) + 1e-5
            loss = numerator / denominator

        return (loss, per_example_loss, log_probs)


    def __gather_indexes(self, sequence_tensor, positions):
        """Gathers the vectors at the specific positions over a minibatch."""
        sequence_shape = get_shape_list(sequence_tensor, expected_rank=3)
        batch_size = sequence_shape[0]
        seq_length = sequence_shape[1]
        width = sequence_shape[2]

        flat_offsets = tf.reshape(tf.range(0, batch_size, dtype=tf.int32) * seq_length, [-1, 1])
        flat_positions = tf.reshape(positions + flat_offsets, [-1])
        flat_sequence_tensor = tf.reshape(sequence_tensor, [batch_size * seq_length, width])
        output_tensor = tf.gather(flat_sequence_tensor, flat_positions)
        return output_tensor
    

    def __metric_fn(self, masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids, masked_lm_weights):
        """Вычисляет потери и точность модели."""
        masked_lm_log_probs = tf.reshape(masked_lm_log_probs, [-1, masked_lm_log_probs.shape[-1]])
        masked_lm_predictions = tf.argmax(masked_lm_log_probs, axis=-1, output_type=tf.int32)

        masked_lm_example_loss = tf.reshape(masked_lm_example_loss, [-1])
        masked_lm_ids = tf.reshape(masked_lm_ids, [-1])
        masked_lm_weights = tf.reshape(masked_lm_weights, [-1])

        masked_lm_accuracy = tf.compat.v1.metrics.accuracy(labels=masked_lm_ids, predictions=masked_lm_predictions, 
                                                            weights=masked_lm_weights)
        masked_lm_mean_loss = tf.compat.v1.metrics.mean(values=masked_lm_example_loss, weights=masked_lm_weights)

        return {
            "masked_lm_accuracy": masked_lm_accuracy,
            "masked_lm_loss": masked_lm_mean_loss,
        }
    

    def __get_predictions(self, masked_lm_log_probs):
        masked_lm_log_probs = tf.reshape(masked_lm_log_probs, [-1, masked_lm_log_probs.shape[-1]])
        masked_lm_predictions = tf.argmax(masked_lm_log_probs, axis=-1, output_type=tf.int32)
        return masked_lm_predictions


if __name__=='__main__':
    rs = RecommSystem(use_logging=True)
    rs.do_predict()