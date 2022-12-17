"""
A python module with functions designed to identify RBs with legendary upside.
"""


# Imports
import pandas as pd
import glob
import os

import merge_dataframes as md


# CSV Constants
YEAR = 2021
RELEVANT_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age']
PLAYER_AGE = f'./{YEAR}_data/data_player_age.csv'
OL_RANK = f'./{YEAR}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR}_data/data_team_trgt%.csv'
PLAYER_ADPS = f'./{YEAR}_data/data_player_adp.csv'
MAIN_RB_CSV = f'./{YEAR}_data/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob(f'./{YEAR}_data/data_rb*.csv') if 'stats' not in file]


def create_rb_csv() -> None:
    """
    Execute the program.
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
    primary_dataframe.to_csv(f'./{YEAR}_data/compiled_rb_data.csv')


def remove_non_legendary_runningbacks(dataframe):
    dataframe = dataframe.loc[dataframe["Fee"] >= 24000 ]


def main() -> None:
    if not os.path.exists(f'./{YEAR}_data/compiled_rb_data.csv'):
        create_rb_csv()
    legendary_runningback_candidates = pd.read_csv(f'./{YEAR}_data/compiled_rb_data.csv', usecols = RELEVANT_COLUMNS, low_memory = True)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, OL_RANK, 0, 1, 'olRank', base_index=1)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, TEAM_TARGETS, 0, 7, 'teamTargets', base_index=1)
    print(legendary_runningback_candidates)


if __name__ == '__main__':
    main()