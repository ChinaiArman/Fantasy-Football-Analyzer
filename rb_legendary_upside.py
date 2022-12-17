"""
A python module with functions designed to identify RBs with legendary upside.
"""


# Imports
import pandas as pd
import glob
import os

import merge_dataframes as md


# CSV Constants
YEAR = 2022
RELEVANT_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age']
PLAYER_AGE = f'./{YEAR - 1}_data/data_player_age.csv'
OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'
PLAYER_ADPS = f'./{YEAR - 1}_data/data_player_adp.csv'
MAIN_RB_CSV = f'./{YEAR - 1}_data/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob(f'./{YEAR - 1}_data/data_rb*.csv') if 'stats' not in file]


def create_rb_csv() -> None:
    """
    Create the RB CSV containing all the RB data.

    :return: None.
    """
    primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')
    dataframes = [md.create_dataframe(file, 'Name', 3) for file in RB_CSVS]
    primary_dataframe = md.create_combined_dataframe(primary_dataframe, dataframes)
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 11, 'ADP')
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
    primary_dataframe = primary_dataframe.sort_values('ADP')
    primary_dataframe = primary_dataframe.dropna(subset=['ADP'])
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.drop('index', axis=1, inplace=True)
    primary_dataframe.to_csv(f'./{YEAR - 1}_data/compiled_rb_data.csv')


def remove_non_legendary_runningbacks(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove RBs that do not have legendary upside from a DataFrame.
    
    """
    dataframe['trgt%'] = (dataframe['recTarg'] / ((dataframe['teamTargets'] / 17) * dataframe['games'])) * 100
    dataframe = dataframe[dataframe['ADP'] <= 26]
    dataframe = dataframe[ 
        ((dataframe['trgt%'] >= 9) & (dataframe['age'] <= 22)) |
        ((dataframe['trgt%'] >= 11) & (dataframe['age'] <= 23)) |
        ((dataframe['trgt%'] >= 13) & (dataframe['age'] <= 24)) |
        ((dataframe['trgt%'] >= 13) & (dataframe['age'] <= 25)) |
        ((dataframe['trgt%'] >= 15) & (dataframe['age'] <= 26))
        ]
    dataframe = dataframe[dataframe['olRank'] <= 24]
    dataframe = dataframe.drop('teamTargets', axis=1)
    return dataframe


def legendary_runningbacks() -> None:
    if not os.path.exists(f'./{YEAR - 1}_data/compiled_rb_data.csv'):
        create_rb_csv()
    legendary_runningback_candidates = pd.read_csv(f'./{YEAR - 1}_data/compiled_rb_data.csv', usecols = RELEVANT_COLUMNS, low_memory = True)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, OL_RANK, 0, 1, 'olRank', base_index=1)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, TEAM_TARGETS, 0, 7, 'teamTargets', base_index=1)
    legendary_runningbacks = remove_non_legendary_runningbacks(legendary_runningback_candidates)
    if not os.path.exists(f'./{YEAR}_calculations'):
        final_directory = os.path.join(os.getcwd(), f'{YEAR}_calculations')
        os.makedirs(final_directory)
    legendary_runningbacks.to_csv(f'./{YEAR}_calculations/legendary_runningbacks.csv')


if __name__ == '__main__':
    legendary_runningbacks()