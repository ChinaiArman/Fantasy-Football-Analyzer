"""
Arman Chinai

A python script to parse multiple CSV files and create a single CSV file.
"""


import pandas as pd
import glob
import os
import numpy as np


RB_CSVS = [file for file in os.listdir("c:/Users/arman/OneDrive/Documents/GitHub/Fantasy-Football-Analyzer") if file.startswith('data_rb')]
TEAM_CSVS = [file for file in os.listdir("c:/Users/arman/OneDrive/Documents/GitHub/Fantasy-Football-Analyzer") if file.startswith('data_team')]
print(os.getcwd())


def create_combined_csv():
    pass
    # print(RB_CSVS)
    # df = pd.read_csv(RB_CSVS[0])
    # print('hi')
    # print(df.head())
    # print('hey')


def main():
    create_combined_csv()


if __name__ == "__main__":
    main()
