from model.modeling.support_funcs import get_shape_list, get_activation, create_initializer, layer_norm
from termcolor import colored
import tensorflow as tf
import pickle



def get_files_paths(string_with_files_paths:str):
    files_paths = []
    for input_pattern in string_with_files_paths.split(","):
        files_paths.extend(tf.compat.v1.gfile.Glob(input_pattern))
    return files_paths


def show_info_files_paths(text:str, files_paths:list):
    print(text)
    for input_file in files_paths:
        print("  %s" % input_file)


def get_input_files(strings_with_files_paths:list, mode_recomm_system:str):
    if mode_recomm_system == "TRAIN":
        train_input_file = strings_with_files_paths[0]
        train_input_files = get_files_paths(train_input_file)
        show_info_files_paths("*** Входные файлы для тренировки ***", train_input_files)
        return (train_input_files, [], [])
    elif mode_recomm_system == "EVAL":
        test_input_file = strings_with_files_paths[1]
        test_input_files = []
        if test_input_file is None:
            test_input_files = get_files_paths(train_input_file)
        else:
            test_input_files = get_files_paths(test_input_file)
        show_info_files_paths("*** Входные файлы для тестировки ***", test_input_files)
        return ([], test_input_files, [])
    elif mode_recomm_system == "PREDICT":
        predict_input_file = strings_with_files_paths[2]
        predict_input_files = []
        return ([], [], predict_input_files)
    else:
        raise Exception(colored("Неверно указан режим работы системы. Возможные значения: TRAIN, EVAL, PREDICT", "red", attrs=['bold', 'underline']))


def get_item_size_from_vocab(vocab_filename:str):
    try:
        with open(vocab_filename, 'rb') as input_file:
            vocab = pickle.load(input_file)
        
        return len(vocab.counter)
    
    except Exception as e:
        print(colored(f"Ошибка при чтении vocab файла: {e}", "red", attrs=['bold', 'underline']))


def gather_indexes(sequence_tensor, positions):
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


def get_masked_lm_output(bert_config, input_tensor, output_weights, positions, label_ids, label_weights):
    """Get loss and log probs for the masked LM."""
    # [batch_size*label_size, dim]
    input_tensor = gather_indexes(input_tensor, positions)

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

        one_hot_labels = tf.one_hot(
            label_ids, depth=output_weights.shape[0], dtype=tf.float32)

        # The `positions` tensor might be zero-padded (if the sequence is too
        # short to have the maximum number of predictions). The `label_weights`
        # tensor has a value of 1.0 for every real prediction and 0.0 for the
        # padding predictions.
        per_example_loss = -tf.reduce_sum(
            log_probs * one_hot_labels, axis=[-1])
        numerator = tf.reduce_sum(label_weights * per_example_loss)
        denominator = tf.reduce_sum(label_weights) + 1e-5
        loss = numerator / denominator

    return (loss, per_example_loss, log_probs)


def metric_fn(masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids, masked_lm_weights):
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


def decode_record(record, name_to_features):
    """Decodes a record to a TensorFlow example."""
    example = tf.compat.v1.parse_single_example(record, name_to_features)

    # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
    # So cast all int64 to int32.
    for name in list(example.keys()):
        t = example[name]
        if t.dtype == tf.int64:
            t = tf.compat.v1.to_int32(t)
        example[name] = t

    return example