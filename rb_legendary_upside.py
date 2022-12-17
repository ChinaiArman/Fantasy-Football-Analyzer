"""
A python module with functions designed to identify RBs with legendary upside.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
RELEVANT_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age']
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
        ((dataframe['trgt%'] >= 9) & (dataframe['age'] <= 22)) |
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
    legendary_runningback_candidates = pd.read_csv(f'./{YEAR - 1}_data/compiled_rb_data.csv', usecols = RELEVANT_COLUMNS, low_memory = True)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, OL_RANK, 0, 1, 'olRank', base_index = 1)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)
    legendary_runningbacks = remove_non_legendary_rbs(legendary_runningback_candidates)
    legendary_runningbacks.reset_index(inplace=True)
    legendary_runningbacks.drop('index', axis=1, inplace=True)
    if not os.path.exists(f'./{YEAR}_calculations'):
        final_directory = os.path.join(os.getcwd(), f'{YEAR}_calculations')
        os.makedirs(final_directory)
    legendary_runningbacks.to_csv(f'./{YEAR}_calculations/legendary_runningbacks.csv')


if __name__ == '__main__':
    main()
