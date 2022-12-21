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

# Extra Datapoints
TEAM_OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'
PLAYER_RUSH_GRADES = f'./{YEAR - 1}_data/data_player_rushgrade.csv'

# Legendary RBs
LEGENDARY_RB_FILE = f'./{YEAR}_calculations/legendary_runningbacks.csv'
LEGENDARY_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'olRank', 'teamTargets']

# Deadzone RBs
DEADZONE_RB_FILE = f'./{YEAR}_calculations/deadzone_runningbacks.csv'
DEADZONE_RB_REL_COLUMNS = ['player', 'team', 'games', 'recTarg', 'ADP', 'age', 'rushCarries', 'olRank', 'teamTargets', 'rushGrade', 'forcedMissedTackles']

# Hero RB Pairs
HERO_RB_FILE = f'./{YEAR}_calculations/hero_runningbacks.csv'
HERO_RB_REL_COLUMNS = ['player', 'team', 'games', 'ADP', 'age', 'rushGrade']


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
    removable_elements = [element for element in dataframe.columns if element not in ['player', 'team', 'age', 'ADP']]
    dataframe = dataframe.drop((element for element in removable_elements), axis=1)
    return dataframe


def remove_deadzone_rbs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove RBs that fall victim to the 'Deadzone' (middle round RBs) from a DataFrame.
    
    :param dataframe: A dataframe containing RB player data.
    :return: A dataframe, containing the RBs that have the upside to overcome the 'Deadzone'.
    """
    dataframe['trgt%'] = (dataframe['recTarg'] / ((dataframe['teamTargets'] / 17) * dataframe['games'])) * 100
    dataframe['evadeRate'] = (dataframe['forcedMissedTackles'] / dataframe['rushCarries']) * 100
    dataframe = dataframe[(dataframe['ADP'] >= 27) & (dataframe['ADP'] <= 80)]
    dataframe = dataframe[ 
        (dataframe['trgt%'] >= 12) |
        ((dataframe['rushGrade'] >= 80) & (dataframe['olRank'] <= 16)) |
        ((dataframe['rushGrade'] >= 70) & (dataframe['evadeRate'] >= 15) & (dataframe['olRank'] <= 10))
        ]
    dataframe = dataframe[dataframe['age'] <= 27]
    removable_elements = [element for element in dataframe.columns if element not in ['player', 'team', 'age', 'ADP']]
    dataframe = dataframe.drop((element for element in removable_elements), axis=1)
    return dataframe


def remove_non_hero_rb_pairs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove RBs that would not serve as good 'Hero RB' pairs (late round RBs) from a DataFrame.
    
    :param dataframe: A dataframe containing RB player data.
    :return: A dataframe, containing the RBs that can be 'Hero RB' pairings.
    """
    dataframe = dataframe[(dataframe['ADP'] >= 81) & (dataframe['ADP'] <= 120)]
    dataframe = dataframe[dataframe['age'] <= 26]
    dataframe = dataframe[dataframe['rushGrade'] >= 80]
    removable_elements = [element for element in dataframe.columns if element not in ['player', 'team', 'age', 'ADP']]
    dataframe = dataframe.drop((element for element in removable_elements), axis=1)
    return dataframe


def main() -> None:
    """
    Execute the program.
    """
    # LEGENDARY RUNNINGBACKS
    # Read the relevant columns from the RB Data and store as a Pandas DataFrame.
    legendary_runningback_candidates = pd.read_csv(COMPILED_RB_DATA, usecols = LEGENDARY_RB_REL_COLUMNS, low_memory = True)

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


    # DEADZONE RUNNINGBACKS
    # Read the relevant columns from the RB Data and store as a Pandas DataFrame.
    deadzone_runningback_candidates = pd.read_csv(COMPILED_RB_DATA, usecols = DEADZONE_RB_REL_COLUMNS, low_memory = True)

    # Remove RBs that do not meet the criteria for Deadzone Upside.
    deadzone_runningback = remove_deadzone_rbs(deadzone_runningback_candidates)

    # Fix Indexes.
    deadzone_runningback.reset_index(inplace=True)
    deadzone_runningback.drop('index', axis=1, inplace=True)

    # Push to CSV file.
    deadzone_runningback.to_csv(DEADZONE_RB_FILE)

    # HERO RUNNINGBACK PAIRS
    # Read the relevant columns from the RB Data and store as a Pandas DataFrame.
    hero_runningback_candidates = pd.read_csv(COMPILED_RB_DATA, usecols = HERO_RB_REL_COLUMNS, low_memory = True)
    
    # Remove RBs that do not meet the criteria for Deadzone Upside.
    hero_runningback = remove_non_hero_rb_pairs(hero_runningback_candidates)

    # Fix Indexes.
    hero_runningback.reset_index(inplace=True)
    hero_runningback.drop('index', axis=1, inplace=True)

    # # Push to CSV file.
    hero_runningback.to_csv(HERO_RB_FILE) 


if __name__ == '__main__':
    main()
