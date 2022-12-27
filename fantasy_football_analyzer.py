"""
A python-based application to analyze fantasy football players and project their performance for the upcoming season.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md
import rb_analysis as rba
import wr_analysis as wra


# Year Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'

# Team Constants
TEAM_OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'

# Player Constants
PLAYER_AGE = f'./{YEAR - 1}_data/data_player_age.csv'
PLAYER_ADPS = f'./{YEAR - 1}_data/data_player_adp.csv'
PLAYER_PASS_GRADE = f'./{YEAR - 1}_data/data_player_passgrade.csv'
PLAYER_RUSH_GRADES = f'./{YEAR - 1}_data/data_player_rushgrade.csv'
PLAYER_REC_GRADE = f'./{YEAR - 1}_data/data_player_receivinggrade.csv'

# RB Constants
COMPILED_RB_DATA = f'./{YEAR - 1}_data/compiled_rb_data.csv'
NECESSARY_RB_COLUMNS = ['player', 'team', 'games', 'recTarg', 'rushCarries']
LEGENDARY_RB_FILE = f'./{YEAR}_calculations/legendary_runningbacks.csv'
LEGENDARY_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'olRank', 'teamTargets']
DEADZONE_RB_FILE = f'./{YEAR}_calculations/deadzone_runningbacks.csv'
DEADZONE_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'rushCarries', 'olRank', 'teamTargets', 'rushGrade', 'forcedMissedTackles']
HERO_RB_FILE = f'./{YEAR}_calculations/hero_runningbacks.csv'
HERO_RB_REL_COLUMNS = ['player', 'team', 'games', 'ADP', 'age', 'rushGrade']
MAIN_RB_CSV = f'./{YEAR - 1}_data/data_rb_stats.csv'

# WR Constants
COMPILED_WR_DATA = f'./{YEAR - 1}_data/compiled_wr_data.csv'
NECESSARY_WR_COLUMNS = ['player', 'team', 'games', 'recTarg']
BREAKOUT_WR_FILE = f'./{YEAR}_calculations/breakout_receivers.csv'
BREAKOUT_WR_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'teamTargets', 'recGrade']
MAIN_WR_CSV = f'./{YEAR - 1}_data/data_wr_stats.csv'


# QB Constants
COMPILED_QB_DATA = f'./{YEAR - 1}_data/compiled_qb_data.csv'
NECESSARY_QB_COLUMNS = ['player', 'team', 'games', 'rushCarries', 'depthAim']
MUST_DRAFT_QBS_FILE = f'./{YEAR}_calculations/must_draft_quarterbacks.csv'
MUST_DRAFT_QB_REL_COLUMNS = []
MAIN_QB_CSV = f'./{YEAR - 1}_data/data_qb_stats.csv'


def create_rb_csv() -> None:
    """
    Create a containing all the RB data for RBs with an ADP.

    :return: None.
    """
    if not os.path.exists(COMPILED_RB_DATA):
        primary_dataframe = pd.read_csv(MAIN_RB_CSV, usecols = NECESSARY_RB_COLUMNS)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, TEAM_OL_RANK, 0, 1, 'olRank', base_index = 1)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_RUSH_GRADES, 0, 28, 'rushGrade', base_index = 0)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_RUSH_GRADES, 0, 6, 'forcedMissedTackles', base_index = 0)
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
        primary_dataframe = pd.read_csv(MAIN_WR_CSV, usecols = NECESSARY_WR_COLUMNS)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)
        primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_REC_GRADE, 0, 21, 'recGrade', base_index = 0)
        primary_dataframe = primary_dataframe.sort_values('ADP')
        primary_dataframe = primary_dataframe.dropna(subset=['ADP'])
        primary_dataframe.reset_index(inplace=True)
        primary_dataframe.drop('index', axis=1, inplace=True)
        primary_dataframe.to_csv(COMPILED_WR_DATA)

    
def create_qb_csv() -> None:
    """
    Create a containing all the QB data for QBs with an ADP.

    :return: None.
    """
    # if not os.path.exists(COMPILED_QB_DATA):
    primary_dataframe = pd.read_csv(MAIN_QB_CSV, usecols = NECESSARY_QB_COLUMNS)
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, PLAYER_PASS_GRADE, 0, 23, 'offenseGrade')
    primary_dataframe = md.add_extra_datapoints(primary_dataframe, TEAM_OL_RANK, 0, 1, 'olRank', base_index = 1)
    primary_dataframe = primary_dataframe.sort_values('ADP')
    primary_dataframe = primary_dataframe.dropna(subset=['ADP'])
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.drop('index', axis=1, inplace=True)
    primary_dataframe.to_csv(COMPILED_QB_DATA)


def create_analytical_function(stat_file: str, rel_columns: list, file_name: str, analyzer):
    """
    Create a function that generates a filtered CSV from using conditions.

    :param stat_file: A string containing the name of a file used to gather initial statistics from.
    :param rel_columns: A list containing strings representing the names of columns to use from the CSV.
    :param file_name: The name of the file to push the filtered CSV to.
    :param analyzer: The name of a function to apply on the DataFrame, which will filter the original CSV and created a parsed DataFrame.
    :return: A function.
    """
    def analysis() -> None:
        """
        Turn a CSV into a DataFrame, analyze it, and create a new CSV containing rows that only meet specific conditions.
        """
        player_candidates = pd.read_csv(stat_file, usecols = rel_columns, low_memory = True)
        qualified_players = analyzer(player_candidates)
        qualified_players.reset_index(inplace=True)
        qualified_players.drop('index', axis=1, inplace=True)
        if not os.path.exists(CALCULATIONS_FOLDER):
            final_directory = os.path.join(os.getcwd(), CALCULATIONS_FOLDER)
            os.makedirs(final_directory)
        qualified_players.to_csv(file_name)
    return analysis


def main() -> None:
    """
    Execute the program.
    """
    # Create Compiled Data CSVs
    create_rb_csv()
    create_wr_csv()
    create_qb_csv()

    # Create player analysis functions.
    legendary_runningbacks = create_analytical_function(COMPILED_RB_DATA, LEGENDARY_RB_REL_COLUMNS, LEGENDARY_RB_FILE, rba.remove_non_legendary_rbs)
    deadzone_runningbacks = create_analytical_function(COMPILED_RB_DATA, DEADZONE_RB_REL_COLUMNS, DEADZONE_RB_FILE, rba.remove_deadzone_rbs)
    hero_pair_runningbacks = create_analytical_function(COMPILED_RB_DATA, HERO_RB_REL_COLUMNS, HERO_RB_FILE, rba.remove_non_hero_rb_pairs)
    breakout_receivers = create_analytical_function(COMPILED_WR_DATA, BREAKOUT_WR_REL_COLUMNS, BREAKOUT_WR_FILE, wra.remove_non_breakout_wr)

    # Execute player analysis functions.
    legendary_runningbacks()
    deadzone_runningbacks()
    hero_pair_runningbacks()
    breakout_receivers()


if __name__ == '__main__':
    main()
