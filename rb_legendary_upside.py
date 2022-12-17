"""
A python module with functions designed to identify RBs with legendary upside.
"""


# Imports
import pandas as pd
import glob

import merge_dataframes as md


# CSV Constants
YEAR = 2021
PLAYER_AGE = f'./{YEAR}_data/data_player_age.csv'
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
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.drop('index', axis=1, inplace=True)
    primary_dataframe.to_csv(f'./{YEAR}_data/compiled_rb_data.csv')


def main() -> None:
    create_rb_csv()


if __name__ == '__main__':
    main()