"""
A python module with functions able to parse multiple CSV files and create a single CSV file.

REQUIREMENTS FOR CSVS:
- CSVs must only contain data for one 'position' (i.e. only RB data, only team data, etc.).
- CSVs must have unique column headers.
- All CSVs must have the same players.
"""


# Imports
import pandas as pd


# Constants
YEAR = 2022
NECESSARY_RB_COLUMNS = ['player', 'team', 'games', 'recTarg', 'rushCarries']
TEAM_OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'
PLAYER_RUSH_GRADES = f'./{YEAR - 1}_data/data_player_rushgrade.csv'
PLAYER_AGE = f'./{YEAR - 1}_data/data_player_age.csv'
PLAYER_ADPS = f'./{YEAR - 1}_data/data_player_adp.csv'
MAIN_RB_CSV = f'./{YEAR - 1}_data/data_rb_stats.csv'


def add_extra_datapoints(base_data: pd.DataFrame, csv_name: str, identifier_index: int, added_index: int, column_name: str, base_index: int=0) -> pd.DataFrame:
    """
    Add a single column to the base_data DataFrame.

    :param base_data: A Pandas DataFrame.
    :param csv_name: A string representing the name of the CSV to add a column from.
    :param identifier_index: An integer representing the index to use as an identifier to match with base_data. 
    :param added_index: An integer representing the index of the column to add to the Pandas DataFrame.
    :param column_name: An identifier to name the column in the Pandas DataFrame.
    :param base_index: The column in the base DataFrame to match the two DataFrames with (default 0)
    :return: base_data with an added column containing additional data.
    """
    base_identifiers = base_data.iloc[:, base_index]
    df = pd.read_csv(csv_name)
    identifiers_in_csv = [identifier for identifier in df.iloc[:, identifier_index]]


    def map_identifiers_in_csv(identifier: str) -> int:
        """
        Return the player data from the column being added to the player_data DataFrame.

        :param identifier: A string containing an identifier from the adp DataFrame.
        :return: A value representing the additional player information, or None if the player does not exist in the additional DataFrame.
        """
        if identifier in identifiers_in_csv:
            return df.iloc[identifiers_in_csv.index(identifier), added_index]
        else:
            return

            
    base_data[column_name] = list(map(map_identifiers_in_csv, base_identifiers))
    return base_data
    

def main() -> None:
    """
    Execute the program.
    """
    # Create primary DataFrame.
    primary_dataframe = pd.read_csv(MAIN_RB_CSV, usecols = NECESSARY_RB_COLUMNS).sort_values('player')

    # Add extra columns.
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 5, 'ADP')
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')
    primary_dataframe = add_extra_datapoints(primary_dataframe, TEAM_OL_RANK, 0, 1, 'olRank', base_index = 1)
    primary_dataframe = add_extra_datapoints(primary_dataframe, TEAM_TARGETS, 0, 7, 'teamTargets', base_index = 1)
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_RUSH_GRADES, 0, 28, 'rushGrade', base_index = 0)
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_RUSH_GRADES, 0, 6, 'forcedMissedTackles', base_index = 0)

    # Sort by ADP.
    primary_dataframe = primary_dataframe.sort_values('ADP')
    primary_dataframe = primary_dataframe.dropna(subset=['ADP'])

    # Fix indexes.
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.drop('index', axis=1, inplace=True)

    # Move to csv.
    primary_dataframe.to_csv(f'./{YEAR - 1}_data/compiled_rb_data.csv')


if __name__ == "__main__":
    main()
