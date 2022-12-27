"""
A python module with functions designed to identify breakout WRs.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'
COMPILED_WR_DATA = f'./{YEAR - 1}_data/compiled_wr_data.csv'
BREAKOUT_WR_FILE = f'./{YEAR}_calculations/breakout_receivers.csv'
BREAKOUT_WR_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'teamTargets', 'recGrade']


def remove_non_breakout_wr(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove WRs that do not have breakout potential from a DataFrame.
    
    :param dataframe: A dataframe containing WR player data.
    :return: A dataframe, containing the WRs that have breakout potential.
    """
    dataframe['trgt%'] = (dataframe['recTarg'] / ((dataframe['teamTargets'] / 17) * dataframe['games'])) * 100
    dataframe = dataframe[(dataframe['ADP'] >= 30) & (dataframe['ADP'] <= 100)]
    dataframe = dataframe[dataframe['trgt%'] >= 20]
    dataframe = dataframe[dataframe['recGrade'] >= 75]
    dataframe = dataframe[dataframe['age'] <= 25]
    removable_elements = [element for element in dataframe.columns if element not in ['player', 'team', 'age', 'ADP']]
    dataframe = dataframe.drop((element for element in removable_elements), axis=1)
    return dataframe


def main() -> None:
    # BREAKOUT RECEIVERS
    # Read the relevant columns from the WR Data and store as a Pandas DataFrame.
    breakout_receiver_candidates = pd.read_csv(COMPILED_WR_DATA, usecols = BREAKOUT_WR_REL_COLUMNS, low_memory = True)

    # Remove WRs that do not meet the criteria for Breakout Potential.
    breakout_receivers = remove_non_breakout_wr(breakout_receiver_candidates)

    # Fix Indexes.
    breakout_receivers.reset_index(inplace=True)
    breakout_receivers.drop('index', axis=1, inplace=True)

    # Push to CSV file.
    if not os.path.exists(CALCULATIONS_FOLDER):
        final_directory = os.path.join(os.getcwd(), CALCULATIONS_FOLDER)
        os.makedirs(final_directory)
    breakout_receivers.to_csv(BREAKOUT_WR_FILE)


if __name__ == '__main__':
    main()
