import argparse
import pickle

import word2vec as w2v
from relational_embedder import composition
from relational_embedder.composition import CompositionStrategy


if __name__ == "__main__":
    print("Invoke composition of relational embedding")

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--we_model', help='path to we model')
    parser.add_argument('--method', default='avg', help='composition method')
    parser.add_argument('--dataset', help='path to csv files')
    parser.add_argument('--output', default='textified.pkl', help='place to output relational embedding')

    args = parser.parse_args()

    we_model = w2v.load(args.we_model)

    method = None
    if args.method == "avg":
        method = CompositionStrategy.AVG
    elif args.method == "avg_unique":
        method = CompositionStrategy.AVG_UNIQUE

    relational_embedding = composition.compose_dataset(args.dataset, we_model, strategy=method)
    with open(args.output, 'wb') as f:
        pickle.dump(relational_embedding, f)
    print("Relational Embedding serialized to: " + str(args.output))
