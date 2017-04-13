from dataaccess import csv_access
from sklearn.feature_extraction.text import CountVectorizer
from preprocessing import text_processor as tp
from preprocessing import utils_pre as U
import pickle
from architectures import multiclass_classifier as mc
import numpy as np
import itertools
from collections import defaultdict
import gzip


"""
Create training data
"""


def extract_labeled_data_from_files(files, vocab_dictionary, location_dic=None, inv_location_dic=None):
    # Configure countvectorizer with prebuilt dictionary
    tf_vectorizer = CountVectorizer(max_df=1., min_df=0,
                                    encoding='latin1',
                                    tokenizer=lambda text: tp.tokenize(text, ","),
                                    vocabulary=vocab_dictionary,
                                    stop_words='english')

    # configure custom vectorizer
    vectorizer = tp.CustomVectorizer(tf_vectorizer)

    # build location indexes
    if location_dic is None and inv_location_dic is None:
        location_dic, inv_location_dic = U.get_location_dictionary_from_files(files)

    for f in files:
        it = csv_access.csv_iterator_with_header(f)
        for tuple in it:
            clean_tokens = tp.tokenize(tuple, ",")
            clean_tuple = ",".join(clean_tokens)
            x = vectorizer.get_vector_for_tuple(clean_tuple)
            y = location_dic[f]
            yield x, y, clean_tuple, f


def extract_labeled_data(path_of_csvs, vocab_dictionary, location_dic=None, inv_location_dic=None):

    # build location indexes
    if location_dic is None and inv_location_dic is None:
        location_dic, inv_location_dic = U.get_location_dictionary(path_of_csvs)

    # Get files in path
    files = csv_access.list_files_in_directory(path_of_csvs)

    extract_labeled_data_from_files(files,
                                    vocab_dictionary,
                                    location_dic=location_dic,
                                    inv_location_dic=inv_location_dic)


def extract_labeled_data_combinatorial_method(path_of_csvs, vocab_dictionary, location_dic=None, inv_location_dic=None):
    # Configure countvectorizer with prebuilt dictionary
    tf_vectorizer = CountVectorizer(max_df=1., min_df=0,
                                    encoding='latin1',
                                    tokenizer=lambda text: tp.tokenize(text, ","),
                                    vocabulary=vocab_dictionary,
                                    stop_words='english')

    # configure custom vectorizer
    vectorizer = tp.CustomVectorizer(tf_vectorizer)

    # build location indexes
    if location_dic is None and inv_location_dic is None:
        location_dic, inv_location_dic = U.get_location_dictionary(path_of_csvs)

    # Get files in path
    files = csv_access.list_files_in_directory(path_of_csvs)
    for f in files:
        print("Processing: " + str(f))
        it = csv_access.csv_iterator_with_header(f)
        location_vocab = set()
        # First build dictionary of location
        for tuple in it:
            clean_tokens = tp.tokenize(tuple, ",")
            for ct in clean_tokens:
                location_vocab.add(ct)

        for t1, t2, t3, t4 in itertools.combinations(location_vocab, 4):
            clean_tuple = ",".join([t1, t2, t3, t4])
            x = vectorizer.get_vector_for_tuple(clean_tuple)
            y = location_dic[f]
            yield x, y, clean_tuple, f

"""
Train model
"""


def train_model(training_data_file, vocab_dictionary, location_dictionary,
                output_path=None, batch_size=128, steps_per_epoch=128):
    input_dim = len(vocab_dictionary)
    output_dim = len(location_dictionary)
    print("Create model with input size: " + str(input_dim) + " output size: " + str(output_dim))
    model = mc.declare_model(input_dim, output_dim)
    model = mc.compile_model(model)

    def incr_data_gen(batch_size):
        # FIXME: this can probably just be an iterable
        while True:
            f = gzip.open(training_data_file, "rb")
            try:
                while True:
                    current_batch_size = 0
                    #current_batch_x = []
                    #current_batch_y = []

                    x, y = pickle.load(f)
                    current_batch_x = np.asarray([(x.toarray())[0]])
                    dense_target = [0] * len(location_dictionary)
                    dense_target[y] = 1
                    current_batch_y = np.asarray([dense_target])
                    current_batch_size += 1

                    while current_batch_size < batch_size:
                        x, y = pickle.load(f)
                        dense_array = np.asarray([(x.toarray())[0]])
                        dense_target = [0] * len(location_dictionary)
                        dense_target[y] = 1
                        dense_target = np.asarray([dense_target])
                        current_batch_x = np.concatenate((current_batch_x, dense_array))
                        current_batch_y = np.concatenate((current_batch_y, dense_target))
                        current_batch_size += 1
                    #yield dense_array, dense_target
                    yield current_batch_x, current_batch_y
            except EOFError:
                print("All input is now read")
                f.close()

    trained_model = mc.train_model_incremental(model, incr_data_gen(batch_size), epochs=10, steps_per_epoch=steps_per_epoch)

    if output_path is not None:
        mc.save_model_to_path(trained_model, output_path)
        print("Model saved to: " + str(output_path))


"""
Test model with same training data
"""


def test_model(model, training_data_file, location_dictionary):
    def incr_data_gen():
        while True:
            f = open(training_data_file, "rb")
            try:
                while True:
                    x, y = pickle.load(f)
                    dense_array = np.asarray([(x.toarray())[0]])
                    dense_target = [0] * len(location_dictionary)
                    dense_target[y] = 1
                    dense_target = np.asarray([dense_target])
                    yield dense_array, dense_target
            except EOFError:
                print("All input is now read")
                f.close()
    score = mc.evaluate_model_incremental(model, incr_data_gen(), steps=10000)
    print(score)


if __name__ == "__main__":
    print("Conductor")

    mit_dwh_vocab = U.get_tf_dictionary("/Users/ra-mit/development/fabric/data/statistics/mitdwhall_tf_only")

    f = gzip.open("/Users/ra-mit/development/fabric/data/mitdwh/training/training_comb.data.pklz", "wb")
    #f = open("/Users/ra-mit/development/fabric/data/mitdwh/training/training_comb.data.pklz", "wb")
    #g = open("/Users/ra-mit/development/fabric/data/mitdwh/training/training_comb_readable.dat", "w")
    i = 1
    sample_dic = defaultdict(int)
    for x, y, tuple, location in extract_labeled_data_combinatorial_method("/Users/ra-mit/data/mitdwhdata", mit_dwh_vocab):
        if i % 50000 == 0:
            print(str(i) + " samples generated \r",)
            #exit()
        pickle.dump((x, y), f)
        #g.write(str(tuple) + " - " + str(location) + "\n")
        sample_dic[location] += 1
        i += 1
    f.close()
    #g.close()

    sorted_samples = sorted(sample_dic.items(), key=lambda x: x[1], reverse=True)
    for el in sorted_samples:
        print(str(el))

    print("Done!")

    exit()

    f = gzip.open("/Users/ra-mit/development/fabric/data/mitdwh/training/training_comb.data.pklz", "rb")

    i = 0
    try:
        while True:
            i += 1
            x, y = pickle.load(f)
            print(str(x))
            print(str(y))
    except EOFError:
        print("All input is now read")
        exit()

    mit_dwh_vocab = U.get_tf_dictionary("/Users/ra-mit/development/fabric/data/statistics/mitdwhall_tf_only")
    location_dic, inv_location_dic = U.get_location_dictionary("/Users/ra-mit/data/mitdwhdata")

    train_model("/Users/ra-mit/development/fabric/data/mitdwh/training/training.data", mit_dwh_vocab, location_dic)

    #model = mc.load_model_from_path("/Users/ra-mit/development/fabric/data/mitdwh/training/trmodel.h5")

    #test_model(model, "/Users/ra-mit/development/fabric/data/mitdwh/training/training.data", location_dic)
