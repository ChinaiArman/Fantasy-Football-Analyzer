"""
A python module with functions designed to identify QBs that are likely to serve as QB1s for the upcoming season.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'
COMPILED_QB_DATA = f'./{YEAR - 1}_data/compiled_qb_data.csv'
MUST_DRAFT_QB_FILE = f'./{YEAR}_calculations/must_draft_quarterbacks.csv'
MUST_DRAFT_QB_REL_COLUMNS = ['player', 'team', 'games', 'ADP', 'age', 'rushCarries', 'depthAim', 'olRank', 'offenseGrade']


def remove_non_breakout_qbs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove QBs that are unlikely to serve as a QB1/ have good ROI for the upcoming season.
    
    :param dataframe: A dataframe containing QB player data.
    :return: A dataframe, containing the QBs that will have good ROI.
    """
    dataframe['rushPerGame'] = (dataframe['rushCarries'] / dataframe['games'])
    dataframe = dataframe[
        ((dataframe['rushPerGame'] >= 5) & (dataframe['depthAim'] >= 9.0)) |
        ((dataframe['age'] <= 30) & (dataframe['offenseGrade'] >= 90)) |
        ((dataframe['ADP'] <= 30))
        ]
    removable_elements = [element for element in dataframe.columns if element not in ['player', 'team', 'age', 'ADP']]
    dataframe = dataframe.drop((element for element in removable_elements), axis=1)
    return dataframe


def main() -> None:
    # MUST DRAFT QBs
    # Read the relevant columns from the QB Data and store as a Pandas DataFrame.
    must_draft_qb_candidates = pd.read_csv(COMPILED_QB_DATA, usecols = MUST_DRAFT_QB_REL_COLUMNS, low_memory = True)

    # Remove QBs that do not meet the criteria for being Must Drafts.
    must_draft_qbs = remove_non_breakout_qbs(must_draft_qb_candidates)

    # Fix Indexes.
    must_draft_qbs.reset_index(inplace=True)
    must_draft_qbs.drop('index', axis=1, inplace=True)
    
    # Push to CSV file.
    if not os.path.exists(CALCULATIONS_FOLDER):
        final_directory = os.path.join(os.getcwd(), CALCULATIONS_FOLDER)
        os.makedirs(final_directory)
    must_draft_qbs.to_csv(MUST_DRAFT_QB_FILE)


if __name__ == '__main__':
    main()
