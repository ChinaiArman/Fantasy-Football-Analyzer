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
COMPILED_RB_DATA = f'./{YEAR - 1}_data/compiled_rb_data.csv'
LEGENDARY_RB_FILE = f'./{YEAR}_calculations/legendary_runningbacks.csv'
LEGENDARY_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age']
OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'


def remove_non_legendary_rbs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove RBs that do not have legendary upside from a DataFrame.
    
    :param dataframe: A dataframe containing RB player data.
    :return: A dataframe, containing the RBs that have 'Legendary Upside'.
    """
    dataframe['trgt%'] = (dataframe['recTarg'] / ((dataframe['teamTargets'] / 17) * dataframe['games'])) * 100
    dataframe = dataframe[dataframe['ADP'] <= 26]
    dataframe = dataframe[ 
        ((dataframe['trgt%'] >= 7) & (dataframe['age'] <= 22)) |
        ((dataframe['trgt%'] >= 11) & (dataframe['age'] <= 23)) |
        ((dataframe['trgt%'] >= 13) & (dataframe['age'] <= 25)) |
        ((dataframe['trgt%'] >= 15) & (dataframe['age'] <= 27))
        ]
    dataframe = dataframe[dataframe['olRank'] <= 24]
    dataframe = dataframe.drop('teamTargets', axis=1)
    return dataframe


def main() -> None:
    """
    Execute the program.
    """
    # Read the relevant columns from the RB Data and store as a Pandas DataFrame.
    legendary_runningback_candidates = pd.read_csv(COMPILED_RB_DATA, usecols = LEGENDARY_RB_REL_COLUMNS, low_memory = True)

    # Add extra datapoints necessary for Legendary RB Calculations.
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, OL_RANK, 0, 1, 'olRank', base_index = 1)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)

    # Remove RBs that do not meet the criteria for Legendary Upside.
    legendary_runningbacks = remove_non_legendary_rbs(legendary_runningback_candidates)

    # Fix Indexes.
    legendary_runningbacks.reset_index(inplace=True)
    legendary_runningbacks.drop('index', axis=1, inplace=True)

    # Push to CSV file.
    if not os.path.exists(CALCULATIONS_FOLDER):
        final_directory = os.path.join(os.getcwd(), CALCULATIONS_FOLDER)
        os.makedirs(final_directory)
    legendary_runningbacks.to_csv(LEGENDARY_RB_FILE)


if __name__ == '__main__':
    main()
