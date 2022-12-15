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
PLAYER_ADPS = './CSVs/data_player_adp.csv'
MAIN_RB_CSV = './CSVs/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob('./CSVs/data_rb*.csv') if 'stats' not in file]
IGNORED_COLUMNS = ('Ovr', 'Name', 'Team')


def add_adp_data(player_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column 'ADP' to the player_data DataFrame.

    :param player_data: A Pandas DataFrame.
    :return: player_data with an additional 'ADP' column containing the player's ADP data.
    """
    player_names = player_data.iloc[:, 0]
    adp_df = pd.read_csv(PLAYER_ADPS)
    players_with_adp = [player for player in adp_df.iloc[:, 1]]
    def map_player_adp(player):
        if player in players_with_adp:
            return adp_df.iloc[players_with_adp.index(player), 11]
        else:
            return
    player_data['ADP'] = list(map(map_player_adp, player_names))
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
    for column in IGNORED_COLUMNS:
        df = df.loc[:, df.columns != column]
    return df


def main():
    """
    Execute the program
    """
    dataframes = [create_dataframe(file) for file in RB_CSVS]
    primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')
    primary_dataframe = add_adp_data(create_combined_dataframe(primary_dataframe, dataframes)).sort_values('ADP')
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.to_csv('rb_data_combined.csv')


if __name__ == "__main__":
    main()
