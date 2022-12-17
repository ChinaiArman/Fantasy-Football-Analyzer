"""
A python module with functions designed to identify breakout WRs.
"""


# Imports
import pandas as pd
import os

import merge_dataframes as md


# Constants
YEAR = 2022
CALCULATIONS_FOLDER = f'./{YEAR}_calculations'
COMPILED_WR_DATA = f'./{YEAR - 1}_data/compiled_wr_data.csv'
BREAKOUT_WR_FILE = f'./{YEAR}_calculations/breakout_receivers.csv'
BREAKOUT_WR_REL_COLUMNS = []
# OL_RANK = f'./{YEAR - 1}_data/data_team_olrank.csv'
# TEAM_TARGETS = f'./{YEAR - 1}_data/data_team_trgt%.csv'


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
