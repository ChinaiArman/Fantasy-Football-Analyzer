"""
A python module with functions designed to identify breakout WRs.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
RELEVANT_COLUMNS = []


def create_wr_csv() -> None:
    """
    Create a containing all the WR data for WRs with an ADP.

    :return: None.
    """
    pass


def remove_non_breakout_wr(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove WRs that do not have breakout potential from a DataFrame.
    
    :param dataframe: A dataframe containing WR player data.
    :return: A dataframe, containing the WRs that have breakout potential.
    """
    pass


def main() -> None:
    pass


if __name__ == '__main__':
    main()
