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
PLAYER_AGE = './CSVs/data_player_age.csv'
PLAYER_ADPS = './CSVs/data_player_adp.csv'
MAIN_RB_CSV = './CSVs/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob('./CSVs/data_rb*.csv') if 'stats' not in file]


def add_extra_datapoints(player_data: pd.DataFrame, csv_name, index, column_name) -> pd.DataFrame:
    """
    Add a single column to the player_data DataFrame.

    :param player_data: A Pandas DataFrame.
    :param csv_name: A string representing the name of the CSV to add a column from.
    :param index: An integer representing the index of the column to add to the Pandas DataFrame.
    :param column_name: An identifier to name the column in the Pandas DataFrame.
    :return: player_data with an added column containing additional player data.
    """
    player_names = player_data.iloc[:, 0]
    df = pd.read_csv(csv_name)
    players_in_csv = [player for player in df.iloc[:, 1]]


    def map_players_in_csv(player: str) -> int:
        """
        Return the player data from the column being added to the player_data DataFrame.

        :param: A string containing an identifier from the adp DataFrame.
        :return: A value representing the additional player information, or None if the player does not exist in the additional DataFrame.
        """
        if player in players_in_csv:
            return df.iloc[players_in_csv.index(player), index]
        else:
            return

            
    player_data[column_name] = list(map(map_players_in_csv, player_names))
    return player_data
    


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
    Create a ready-to-concatenate dataframe from a CSV (sorted alphabetically without duplicated headers).

    :param file: A string identifying a csv file within the directory. 
    :return: A Pandas DataFrame, ready to be concatenated.
    """
    df = pd.read_csv(file).sort_values('Name')
    return df.iloc[:, 3:]


def main():
    """
    Execute the program
    """
    dataframes = [create_dataframe(file) for file in RB_CSVS]
    primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')
    primary_dataframe = create_combined_dataframe(primary_dataframe, dataframes)
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 11, 'ADP')
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_AGE, 4, 'age')
    primary_dataframe = primary_dataframe.sort_values('ADP')
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.to_csv('rb_data_combined.csv')


if __name__ == "__main__":
    main()
