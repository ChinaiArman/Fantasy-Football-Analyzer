"""
Arman Chinai

A python script to parse multiple CSV files and create a single CSV file.
"""


import pandas as pd
import glob
import os
import numpy as np


RB_CSVS = [file for file in glob.glob('data_rb*.csv') if 'stats' not in file]
TEAM_CSVS = [file for file in glob.glob('data_team*.csv')]
IGNORED_COLUMNS = ['Ovr', 'Name', 'Team']


def create_dataframe(file):
    df = pd.read_csv(file)
    for column in IGNORED_COLUMNS:
        df = df.loc[:, df.columns != column]
    return df


def main():
    dataframes = [create_dataframe(file) for file in RB_CSVS]
    


if __name__ == "__main__":
    main()
