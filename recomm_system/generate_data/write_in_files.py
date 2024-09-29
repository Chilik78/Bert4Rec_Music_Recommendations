from termcolor import colored
import tensorflow as tf
import collections
import pickle


def create_int_feature(values):
    feature = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
    return feature


def create_float_feature(values):
    feature = tf.train.Feature(
        float_list=tf.train.FloatList(value=list(values)))
    return feature


def write_instance_to_example_files(instances, max_seq_length, max_predictions_per_seq, vocab, output_files):
    """
        Create TF example files from `TrainingInstance`s.
        
        Создает файлы примеров TF из "Обучающего экземпляра".
    """

    writers = []
    for output_file in output_files:
        writers.append(tf.compat.v1.python_io.TFRecordWriter(output_file))

    writer_index = 0

    total_written = 0
    for (inst_index, instance) in enumerate(instances):

        try:
            input_ids = vocab.convert_tokens_to_ids(instance.tokens)
        except:
            print(instance)

        input_mask = [1] * len(input_ids)
        assert len(input_ids) <= max_seq_length

        input_ids += [0] * (max_seq_length - len(input_ids))
        input_mask += [0] * (max_seq_length - len(input_mask))

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length

        masked_lm_positions = list(instance.masked_lm_positions)
        masked_lm_ids = vocab.convert_tokens_to_ids(instance.masked_lm_labels)
        masked_lm_weights = [1.0] * len(masked_lm_ids)

        masked_lm_positions += [0] * (max_predictions_per_seq - len(masked_lm_positions))
        masked_lm_ids += [0] * (max_predictions_per_seq - len(masked_lm_ids))
        masked_lm_weights += [0.0] * (max_predictions_per_seq - len(masked_lm_weights))

        features = collections.OrderedDict()
        features["info"] = create_int_feature(instance.info)
        features["input_ids"] = create_int_feature(input_ids)
        features["input_mask"] = create_int_feature(input_mask)
        features["masked_lm_positions"] = create_int_feature(masked_lm_positions)
        features["masked_lm_ids"] = create_int_feature(masked_lm_ids)
        features["masked_lm_weights"] = create_float_feature(masked_lm_weights)

        tf_example = tf.train.Example(features=tf.train.Features(feature=features))

        writers[writer_index].write(tf_example.SerializeToString())
        writer_index = (writer_index + 1) % len(writers)

        total_written += 1

        if inst_index < 20:
            tf.compat.v1.logging.info("*** Example ***")
            tokens_in_string = " ".join([str(x) for x in instance.tokens])
            tf.compat.v1.logging.info("tokens: " + tokens_in_string)

            for feature_name in features.keys():
                feature = features[feature_name]
                values = []
                if feature.int64_list.value:
                    values = feature.int64_list.value
                elif feature.float_list.value:
                    values = feature.float_list.value


                values_in_string = " ".join([str(x) for x in values])
                tf.compat.v1.logging.info(f"{feature_name}: " + values_in_string)

    for writer in writers:
        writer.close()

    tf.compat.v1.logging.info("Wrote %d total instances", total_written)


def write_other_files(data, text, filename)->None:
    print(colored(text, 'green', attrs=['underline']))
    with open(filename, 'wb') as output_file:
        pickle.dump(data, output_file, protocol=2)