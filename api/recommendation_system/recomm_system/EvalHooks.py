import tensorflow as tf
import numpy as np
import pickle
import sys

class EvalHooks(tf.compat.v1.train.SessionRunHook):
    def __init__(self, is_logging, user_history_filename, vocab_filename, max_predictions_per_seq, use_pop_random):

        self.__is_logging = is_logging
        self.__user_history_filename = user_history_filename
        self.__vocab_filename = vocab_filename
        self.__max_predictions_per_seq = max_predictions_per_seq
        self.__use_pop_random = use_pop_random

        if(is_logging):
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

        if self.__user_history_filename is not None:
            if(self.__is_logging):
                print('load user history from :' + self.__user_history_filename)

            with open(self.__user_history_filename, 'rb') as input_file:
                self.user_history = pickle.load(input_file)

        if self.__vocab_filename is not None:
            if(self.__is_logging):
                print('load vocab from :' + self.__vocab_filename)

            with open(self.__vocab_filename, 'rb') as input_file:
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
        if(self.__is_logging):
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
        masked_lm_log_probs = masked_lm_log_probs.reshape((-1, self.__max_predictions_per_seq, masked_lm_log_probs.shape[1]))

        for idx in range(len(input_ids)):
            key = "user_" + str(info[idx][0])
            if not self.user_history.get(key): continue 
            rated = set(input_ids[idx])
            rated.add(0)
            rated.add(masked_lm_ids[idx][0])
            
            map(lambda x: rated.add(x), self.user_history[key][0])
            item_idx = [masked_lm_ids[idx][0]]
            # here we need more consideration
            masked_lm_log_probs_elem = masked_lm_log_probs[idx, 0]
            size_of_prob = len(self.ids) + 1  # len(masked_lm_log_probs_elem)
            if self.__use_pop_random:
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