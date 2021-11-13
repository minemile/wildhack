import pandas as pd
import numpy as np
import string
import jamspell
import matplotlib.pyplot as plt
from dataset_prepare import ToStrLower, DropDuplicates, FilterByQuantile
from autocompleter import AutoCompleterBaseline, AutoCompleteBySuffix, AutoCompleteByInvertedIndex
from inverted_index import InvertedIndex
from tries import make_trie
import argparse

UPPER_QUANTILE = 0.95
LOWER_QUANTILE = 0.001
SUBSET_DROP = ["wbuser_id", "UQ"]


def parse_args():
    parser = argparse.ArgumentParser(description='prepare data for autocompleter')
    parser.add_argument('--dataset_path', type=str,
                        help='csv dataset path...')

    parser.add_argument('--save_to',
                        type=str,
                        help='save arifacts to...')
    return parser.parse_args()


def create_uq_to_lemma_map(df):
    pass


if __name__ == "__main__":
    args = parse_args()
    col_list = ['wbuser_id', 'UQ', 'cnt', 'lem_uq']
    print(f"Start loading data at {args.dataset_path}")
    df = pd.read_csv(args.dataset_path, usecols=col_list)
    print(f"End loading dataframe. There is {len(df)} rows")

    # filters

    quantile_filter = FilterByQuantile('cnt', UPPER_QUANTILE)
    df = quantile_filter.apply(df)

    drop_duplicates_filter = DropDuplicates(SUBSET_DROP)
    df = drop_duplicates_filter.apply(df)


    popularity = df.groupby("UQ").size().reset_index(name='popularity')









                    