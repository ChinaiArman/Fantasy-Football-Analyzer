"""
A python script to parse multiple CSV files and create a single CSV file.

REQUIREMENTS FOR CSVS:
- CSVs must only contain data for one 'position' (i.e. only RB data, only team data, etc.).
- CSVs must have unique column headers.
- All CSVs must have the same players.
"""


# Imports
import pandas as pd
import glob


# Constants
MAIN_RB_CSV = 'data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob('data_rb*.csv') if 'stats' not in file]
TEAM_CSVS = [file for file in glob.glob('data_team*.csv')]
IGNORED_COLUMNS = ('Ovr', 'Name', 'Team')


def create_combined_dataframe(primary_dataframe: pd.DataFrame, dataframes: list) -> pd.DataFrame:
    """
    Concatenate a list of Pandas DataFrames horizontally.

    :param primary_dataframe: A Pandas DataFrame.
    :param dataframes: A list of DataFrames to be horizontally concatenated to primary_dataframe.
    :return: A Pandas DataFrame containing all of the DataFrames horizontally concatenated together. 
    """
    for dataframe in dataframes:
        primary_dataframe = pd.concat([primary_dataframe, dataframe.set_index(primary_dataframe.index)], axis=1)
    return primary_dataframe


def create_dataframe(file: str) -> pd.DataFrame:
    """
    
    :param file:
    :return:
    """
    df = pd.read_csv(file).sort_values('Name')
    for column in IGNORED_COLUMNS:
        df = df.loc[:, df.columns != column]
    return df


def main():
    """
    Execute the program
    """
    dataframes = [create_dataframe(file) for file in RB_CSVS]
    primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')
    create_combined_dataframe(primary_dataframe, dataframes).to_csv('rb_data_combined.csv')


if __name__ == "__main__":
    main()
