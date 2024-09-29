import tensorflow as tf
from termcolor import colored


if __name__ == '__main__':

    i=0

    COUNT_FOR_BREAK = 10

    test_path = "data/steamdefault.test.tfrecord"
    train_path = "data/steamdefault.train.tfrecord"
    vocab_path = "data/steamdefault.vocab"

    for example in tf.compat.v1.python_io.tf_record_iterator(vocab_path):
        print(colored(tf.train.Example.FromString(example), 'magenta'))
        i+=1

        if(i == COUNT_FOR_BREAK):
            break