from postprocessing import fabric_api
from preprocessing.utils_pre import binary_decode as DECODE
from dataaccess import csv_access
from sklearn.metrics.pairwise import cosine_similarity


import sys
import getopt
import gzip
import pickle
import config
import numpy as np
import os
from os.path import isfile, join
from os import listdir


def get_tokens_from_bin_vector(x):
    tokens = set()
    indices = DECODE(x)
    for index in indices:
        if index == 0:  # reserved for empty buckets
            continue
        term = fabric_api.inv_vocab[index]
        tokens.add(term)
    return tokens


def get_tokens_from_onehot_vector(x):
    tokens = set()
    indices = np.where(x == 1)
    for index in indices[0]:
        if index == 0:  # reserved for empty buckets
            continue
        term = fabric_api.inv_vocab[index]
        tokens.add(term)
    return tokens


def eval_accuracy(path_to_data, encoding_mode, path_to_csv):
    total_samples = 0
    hits = 0
    half_hits = 0
    tokens_missing = 0
    f = gzip.open(path_to_data, "rb")
    try:
        while True:
            x, y = pickle.load(f)
            total_samples += 1

            dense_x = x.toarray()

            if encoding_mode == "index":
                original_tokens = get_tokens_from_bin_vector(dense_x[0])
            else:
                original_tokens = get_tokens_from_onehot_vector(dense_x[0])

            vec_embedding = fabric_api.encode_query_binary("", input_vector=dense_x)

            _, query, token_missing = fabric_api.decode_query_binary(vec_embedding, threshold=0.7)
            if token_missing:
                tokens_missing += 1
            reconstructed_tokens = set(query.split(" "))

            js = len(original_tokens.intersection(reconstructed_tokens)) / \
                 len(original_tokens.union(reconstructed_tokens))
            if js == 1:
                hits += 1
            if js > 0.5:
                half_hits += 1

    except EOFError:
        print("All input is now read")
        f.close()

    print("Training Data ==>")
    hit_ratio = float(hits / total_samples)
    half_hit_ratio = float(half_hits / total_samples)
    print("Hits: " + str(hit_ratio))
    print("Half Hits: " + str(half_hit_ratio))
    print("Total samples: " + str(total_samples))
    print("Tokens missing: " + str(tokens_missing))

    if path_to_csv is None:
        return

    tokens_missing = 0
    total_samples = 0
    hits = 0
    half_hits = 0

    all_files = []
    is_file = os.path.isfile(path_to_csv)
    if not is_file:
        files = [join(path_to_csv, f) for f in listdir(path_to_csv) if isfile(join(path_to_csv, f))]
        for f in files:
            all_files.append(f)

    for f in all_files:
        iterator = csv_access.iterate_columns_no_header(f, token_joiner=" ")
        for data in iterator:
            for tuple in data:
                total_samples += 1
                original_tokens = set(tuple.split(" "))
                vec_embedding = fabric_api.encode_query_binary(tuple)
                _, query, token_missing = fabric_api.decode_query_binary(vec_embedding, threshold=0.7)
                if token_missing:
                    tokens_missing += 1
                reconstructed_tokens = set(query.split(" "))

                js = len(original_tokens.intersection(reconstructed_tokens)) / \
                     len(original_tokens.union(reconstructed_tokens))
                if js == 1:
                    hits += 1
                if js > 0.5:
                    half_hits += 1

    print("Cell Data ==>")
    hit_ratio = float(hits / total_samples)
    half_hit_ratio = float(half_hits / total_samples)
    print("Hits: " + str(hit_ratio))
    print("Half Hits: " + str(half_hit_ratio))
    print("Total samples: " + str(total_samples))
    print("Tokens missing: " + str(tokens_missing))


def eval_similarity(path_to_csv):
    total_samples = 0

    print("Pairwise similarity within columns")
    iterator = csv_access.iterate_columns_no_header(path_to_csv, token_joiner=" ", verbose=True)
    for data in iterator:
        embeddings = []
        for tuple in data:
            total_samples += 1
            vec_embedding = fabric_api.encode_query_binary(tuple)
            embeddings.append(vec_embedding[0])

        sim_matrix = cosine_similarity(np.asarray(embeddings), np.asarray(embeddings))
        avgs = [np.mean(v) for v in sim_matrix]
        total_avg = np.mean(np.asarray(avgs))
        median = np.percentile(avgs, 50)
        p5 = np.percentile(avgs, 5)
        p95 = np.percentile(avgs, 95)
        print("avg: " + str(total_avg) + " median: " + str(median) + " p5: " + str(p5) + " p95: " + str(p95))

    print("Pairwise similarity across columns")
    iterator = csv_access.iterate_columns_no_header(path_to_csv, token_joiner=" ", verbose=True)
    col_embeddings = []
    for data in iterator:
        embeddings = []
        for tuple in data:
            total_samples += 1
            vec_embedding = fabric_api.encode_query_binary(tuple)
            embeddings.append(vec_embedding[0])
        col_embeddings.append(embeddings)
    for i in range(len(col_embeddings)):
        for j in range(len(col_embeddings)):
            sim_matrix = cosine_similarity(np.asarray(col_embeddings[i]), np.asarray(col_embeddings[j]))
            avgs = [np.mean(v) for v in sim_matrix]
            total_avg = np.mean(np.asarray(avgs))
            median = np.percentile(avgs, 50)
            p5 = np.percentile(avgs, 5)
            p95 = np.percentile(avgs, 95)
            stats = (total_avg, median, p5, p95)
            print(str(i) + "->" + str(j) + ": " + str(stats))


def main(path_to_data=None,
         path_to_csv=None,
         path_to_vocab=None,
         path_to_bae_model=None,
         encoding_mode=None,
         topk=2,
         eval_task=None):

    fabric_api.init(path_to_data,
                    path_to_vocab,
                    None,
                    None,
                    None,
                    None,
                    None,
                    path_to_bae_model,
                    encoding_mode,
                    None)

    if eval_task == "accuracy":
        eval_accuracy(path_to_data, encoding_mode, path_to_csv)
    elif eval_task == "similarity":
        eval_similarity(path_to_csv)


if __name__ == "__main__":

    argv = sys.argv[1:]

    ifile = ""
    fabric_path = ""
    encoding_mode = ""
    path_to_csv = ""
    eval_task = "accuracy"  # default

    try:
        opts, args = getopt.getopt(argv, "i:f:", ["encoding=", "csv=", "task="])
    except getopt.GetoptError:
        print("evaluator_fabric.py --encoding=<onehot, index> -i <idata_dir> -f <fabric_dir> --csv=")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("evaluator_fabric.py --encoding=<onehot, index> -i <idata_dir> -f <fabric_dir>")
            sys.exit()
        elif opt in "-i":
            ifile = arg
        elif opt in "-f":
            fabric_path = arg
        elif opt in "--encoding":
            encoding_mode = arg
        elif opt in "--csv":
            path_to_csv = arg
        elif opt in "--task":
            eval_task = arg
    if encoding_mode == "":
        print("Select an encoding mode")
        print("evaluator_fabric.py --encoding=<onehot, index> -i <idata_dir> -f <fabric_dir>")
        sys.exit(2)

    path_to_data = ifile + config.TRAINING_DATA + ".pklz"
    path_to_vocab = ifile + config.TF_DICTIONARY + ".pkl"
    path_to_bae_model = fabric_path
    main(path_to_data=path_to_data,
         path_to_csv=path_to_csv,
         path_to_vocab=path_to_vocab,
         path_to_bae_model=path_to_bae_model,
         encoding_mode=encoding_mode,
         eval_task=eval_task)
