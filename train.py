import argparse
import json
import os
import pickle
import sys

import pandas as pd

from dataset_prepare import DropDuplicates, FilterByQuantile
from inverted_index import InvertedIndex
from tries import make_trie

UPPER_QUANTILE = 0.95
LOWER_QUANTILE = 0.001
SUBSET_DROP = ["wbuser_id", "UQ"]

max_rec = 0x100000
sys.setrecursionlimit(max_rec)
# resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])


def parse_args():
    parser = argparse.ArgumentParser(description="prepare data for autocompleter")
    parser.add_argument("--dataset_path", type=str, help="csv dataset path...")

    parser.add_argument("--save_to", type=str, help="save arifacts to...")
    return parser.parse_args()


def create_uq_to_lemma_map(df, save_to):
    df_ = df.set_index("UQ")
    uq_to_lemma_map = df_["lem_uq"].to_dict()
    with open(os.path.join(save_to, "uq_to_lemma_map.json"), "w") as f:
        json.dump(uq_to_lemma_map, f)
    return uq_to_lemma_map


if __name__ == "__main__":
    args = parse_args()
    col_list = ["wbuser_id", "UQ", "cnt", "lem_uq"]
    print(f"Start loading data at {args.dataset_path}")
    df = pd.read_csv(args.dataset_path, usecols=col_list)
    print(f"End loading dataframe. There is {len(df)} rows")

    # filters
    quantile_filter = FilterByQuantile("cnt", UPPER_QUANTILE)
    df = quantile_filter.apply(df)

    drop_duplicates_filter = DropDuplicates(SUBSET_DROP)
    df = drop_duplicates_filter.apply(df)

    popularity = df.groupby("UQ").size().reset_index(name="popularity")

    uq_to_lemma_map = create_uq_to_lemma_map(df, args.save_to)

    # inverted index
    query_popularity_corpus = zip(popularity["UQ"], popularity["popularity"])
    inverted_index = InvertedIndex(query_to_lemma_map=uq_to_lemma_map)
    index = inverted_index.process_corpus(query_popularity_corpus)

    with open(os.path.join(args.save_to, "inverted_indx.pickle"), "wb") as f:
        pickle.dump(index, f, protocol=pickle.HIGHEST_PROTOCOL)

    # trie
    trie = make_trie(popularity["UQ"].values)
    with open(os.path.join(args.save_to, "trie.pickle"), "wb") as f:
        pickle.dump(trie, f, protocol=pickle.HIGHEST_PROTOCOL)

