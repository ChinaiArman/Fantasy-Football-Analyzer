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
MUST_DRAFT_QB_REL_COLUMNS = ['player', 'team', 'games', 'ADP', 'age']


def remove_non_breakout_qbs(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe


def main():
    # MUST DRAFT QBs
    # Read the relevant columns from the QB Data and store as a Pandas DataFrame.
    must_draft_qb_candidates = pd.read_csv(COMPILED_QB_DATA, usecols = MUST_DRAFT_QB_REL_COLUMNS, low_memory = True)

    # Remove QBs that do not meet the criteria for being Must Drafts.
    must_draft_qbs = remove_non_breakout_qbs(must_draft_qb_candidates)

    # Fix Indexes.
    must_draft_qbs.reset_index(inplace=True)
    must_draft_qbs.drop('index', axis=1, inplace=True)
    print(must_draft_qbs)


if __name__ == '__main__':
    main()