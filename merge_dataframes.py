"""
A python module with functions able to parse multiple CSV files and create a single CSV file.

REQUIREMENTS FOR CSVS:
- CSVs must only contain data for one 'position' (i.e. only RB data, only team data, etc.).
- CSVs must have unique column headers.
- All CSVs must have the same players.
"""


# Imports
import pandas as pd
import glob


# Constants
YEAR = 2021
PLAYER_AGE = f'./{YEAR}_data/data_player_age.csv'
PLAYER_ADPS = f'./{YEAR}_data/data_player_adp.csv'
MAIN_RB_CSV = f'./{YEAR}_data/data_rb_stats.csv'
RB_CSVS = [file for file in glob.glob(f'./{YEAR}_data/data_rb*.csv') if 'stats' not in file]


def add_extra_datapoints(base_data: pd.DataFrame, csv_name: str, identifier_index: int, added_index: int, column_name: str, base_index: int=0) -> pd.DataFrame:
    """
    Add a single column to the base_data DataFrame.

    :param base_data: A Pandas DataFrame.
    :param csv_name: A string representing the name of the CSV to add a column from.
    :param identifier_index: An integer representing the index to use as an identifier to match with base_data. 
    :param added_index: An integer representing the index of the column to add to the Pandas DataFrame.
    :param column_name: An identifier to name the column in the Pandas DataFrame.
    :return: base_data with an added column containing additional data.
    """
    base_identifiers = base_data.iloc[:, base_index]
    df = pd.read_csv(csv_name)
    identifiers_in_csv = [identifier for identifier in df.iloc[:, identifier_index]]


    def map_identifiers_in_csv(identifier: str) -> int:
        """
        Return the player data from the column being added to the player_data DataFrame.

        :param: A string containing an identifier from the adp DataFrame.
        :return: A value representing the additional player information, or None if the player does not exist in the additional DataFrame.
        """
        if identifier in identifiers_in_csv:
            return df.iloc[identifiers_in_csv.index(identifier), added_index]
        else:
            return

            
    base_data[column_name] = list(map(map_identifiers_in_csv, base_identifiers))
    return base_data
    

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


def create_dataframe(file: str, sorting_identifier: str, start: int) -> pd.DataFrame:
    """
    Create a ready-to-concatenate dataframe from a CSV (sorted alphabetically without duplicated headers).

    :param file: A string identifying a csv file within the directory.
    :param sorting_identifier: A string identifying a column within the dataframe to sort by.
    :param start: An integer representing the column from which to keep values from (in order to ignore identifier columns)
    :return: A Pandas DataFrame, ready to be concatenated.
    """
    df = pd.read_csv(file).sort_values(sorting_identifier)
    return df.iloc[:, start:]


def main() -> None:
    """
    Execute the program.
    """
    # Create primary DataFrame.
    primary_dataframe = pd.read_csv(MAIN_RB_CSV).sort_values('player')

    # Create extra DataFrames.
    dataframes = [create_dataframe(file, 'Name', 3) for file in RB_CSVS]

    # Merge DataFrames.
    primary_dataframe = create_combined_dataframe(primary_dataframe, dataframes)

    # Add extra column (ADP).
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_ADPS, 1, 11, 'ADP')

    # Add extra column (age).
    primary_dataframe = add_extra_datapoints(primary_dataframe, PLAYER_AGE, 1, 4, 'age')

    # Sort by ADP.
    primary_dataframe = primary_dataframe.sort_values('ADP')
    primary_dataframe = primary_dataframe.dropna(subset=['ADP'])

    # Fix indexes.
    primary_dataframe.reset_index(inplace=True)
    primary_dataframe.drop('index', axis=1, inplace=True)

    # Move to csv.
    primary_dataframe.to_csv(f'./{YEAR}_data/compiled_rb_data.csv')


if __name__ == "__main__":
    main()
