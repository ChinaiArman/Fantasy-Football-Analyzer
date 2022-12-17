"""
A python-based application to analyze fantasy football players and project their performance for the upcoming season.
"""


# Imports
import pandas as pd
import glob
import os

import merge_dataframes as md
import rb_legendary_upside as rblu
import wr_breakouts as wrb


# Year Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'
OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'

# Player Constants
PLAYER_AGE = f'./{YEAR - 1}_data/data_player_age.csv'
PLAYER_ADPS = f'./{YEAR - 1}_data/data_player_adp.csv'

# RB Constants
COMPILED_RB_DATA = f'./{YEAR - 1}_data/compiled_rb_data.csv'
LEGENDARY_RB_FILE = f'./{YEAR}_calculations/legendary_runningbacks.csv'
LEGENDARY_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age']
MAIN_RB_CSV = f'./{YEAR - 1}_data/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob(f'./{YEAR - 1}_data/data_rb*.csv') if 'stats' not in file]

# WR Constants
COMPILED_WR_DATA = f'./{YEAR - 1}_data/compiled_wr_data.csv'
BREAKOUT_WR_FILE = f'./{YEAR}_calculations/breakout_receivers.csv'
BREAKOUT_WR_REL_COLUMNS = []
MAIN_WR_CSV = f'./{YEAR - 1}_data/data_wr_stats.csv'
WR_CSVS = [file for file in glob.glob(f'./{YEAR - 1}_data/data_wr*.csv') if 'stats' not in file]


def create_rb_csv() -> None:
    """
    Create a containing all the RB data for RBs with an ADP.

    :return: None.
    """
    if not os.path.exists(COMPILED_RB_DATA):
        primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')
        dataframes = [md.create_dataframe(file, 'Name', 3) for file in RB_CSVS]
        primary_dataframe = md.create_combined_dataframe(primary_dataframe, dataframes)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
        primary_dataframe = primary_dataframe.sort_values('ADP')
        primary_dataframe = primary_dataframe.dropna(subset=['ADP'])
        primary_dataframe.reset_index(inplace=True)
        primary_dataframe.drop('index', axis=1, inplace=True)
        primary_dataframe.to_csv(COMPILED_RB_DATA)


def create_wr_csv() -> None:
    """
    Create a containing all the WR data for WRs with an ADP.

    :return: None.
    """
    if not os.path.exists(COMPILED_WR_DATA):
        primary_dataframe = pd.read_csv(MAIN_WR_CSV).sort_values('player')
        dataframes = [md.create_dataframe(file, 'Name', 3) for file in WR_CSVS]
        primary_dataframe = md.create_combined_dataframe(primary_dataframe, dataframes)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
        primary_dataframe = primary_dataframe.sort_values('ADP')
        primary_dataframe = primary_dataframe.dropna(subset=['ADP'])
        primary_dataframe.reset_index(inplace=True)
        primary_dataframe.drop('index', axis=1, inplace=True)
        primary_dataframe.to_csv(COMPILED_WR_DATA)


def legendary_runningbacks() -> None:
    """
    Identify RBs with 'Legendary Upside' and create a CSV to display the result of the calculation.
    
    :return: None.
    """
    legendary_runningback_candidates = pd.read_csv(COMPILED_RB_DATA, usecols = LEGENDARY_RB_REL_COLUMNS, low_memory = True)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, OL_RANK, 0, 1, 'olRank', base_index = 1)
    legendary_runningback_candidates = md.add_extra_datapoints(legendary_runningback_candidates, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)
    legendary_runningbacks = rblu.remove_non_legendary_rbs(legendary_runningback_candidates)
    legendary_runningbacks.reset_index(inplace=True)
    legendary_runningbacks.drop('index', axis=1, inplace=True)
    if not os.path.exists(CALCULATIONS_FOLDER):
        final_directory = os.path.join(os.getcwd(), CALCULATIONS_FOLDER)
        os.makedirs(final_directory)
    legendary_runningbacks.to_csv(LEGENDARY_RB_FILE)


def main() -> None:
    create_rb_csv()
    create_wr_csv()
    legendary_runningbacks()


if __name__ == '__main__':
    main()
