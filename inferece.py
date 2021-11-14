import argparse
import json
import os
import string

import jamspell
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from autocompleter import (
    AutoCompleteByInvertedIndex,
    AutoCompleteBySuffix,
    AutoCompleterBaseline,
)
from dataset_prepare import DropDuplicates, FilterByQuantile, ToStrLower
from inverted_index import InvertedIndex
from tries import make_trie
import pickle

QUERIES_SCORE_THR = 0.1
FIRST_PREFIX = 5
MAX_CANDIDATES = 50


def parse_args():
    parser = argparse.ArgumentParser(description="Autocompleter runner")
    parser.add_argument("--cache_dir", type=str, help="path to cache dir...")
    parser.add_argument("--speller_bin", type=str, help="path to speller bin...")
    parser.add_argument("--query", type=str, help="Type your's query...")
    parser.add_argument("--endless", type=bool, help="run application on user inputs...")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    inverted_index_path = os.path.join(args.cache_dir, "inverted_indx.pickle")
    with open(inverted_index_path, "rb") as fp:
        inverted_index = pickle.load(fp)
    print("Loaded inverted index")

    trie_path = os.path.join(args.cache_dir, "trie.pickle")
    with open(trie_path, "rb") as fp:
        trie = pickle.load(fp)
    print("Loaded trie")

    corrector = jamspell.TSpellCorrector()
    corrector.LoadLangModel(args.speller_bin)
    print("Loaded speller")

    autocomplete_by_inverted_index = AutoCompleteByInvertedIndex(
        inverted_index,
        trie,
        corrector,
        queries_score_thr=QUERIES_SCORE_THR,
        first_prefix=FIRST_PREFIX,
        max_candidates=MAX_CANDIDATES,
    )
    print("Create Autocompleter")

    if args.query:
        queryes = autocomplete_by_inverted_index.query(args.query, max_n=10)
        for query in queryes:
            print(f"Proposal: {query.words}. Score: {query.popularity}")
    else:
        while True:
            query = str(input('Enter query: '))
            queryes = autocomplete_by_inverted_index.query(query, max_n=10)
            for query in queryes:
                print(f"Proposal: {query.words}. Score: {query.popularity}")