"""
A python module with functions designed to identify RBs with legendary upside.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'
COMPILED_QB_DATA = f'./{YEAR - 1}_data/compiled_qb_data.csv'
MUST_DRAFT_QBS_FILE = f'./{YEAR}_calculations/must_draft_quarterbacks.csv'
MUST_DRAFT_QB_REL_COLUMNS = ['player', 'team', 'games', 'adp', 'age']


def remove_non_breakout_qbs(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe


def main():
    pass


if __name__ == '__main__':
    main()