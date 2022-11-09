"""
Add all transformations from the raw tabular dataset to the preprocessed version here
"""
import pandas as pd
import numpy as np


def mirror_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    function that takes a dataframe and mirrors the shot coordinates
    if the shot is in a negative x coordinate
    """
    df = df.copy(deep=True)
    x, y = df['x_coords'], df['y_coords']

    is_x_negative = df['x_coords'] < 0

    df.loc[is_x_negative, 'x_coords'] = -x
    df.loc[is_x_negative, 'y_coords'] = -y

    return df


def append_shot_distance(df: pd.DataFrame, goal_position=(89, 0)) -> pd.DataFrame:
    """
    function that takes a row of a dataframe and appends the shot to goal distance
    in euclidean norm
    """
    df = df.copy(deep=True)

    x, y = df['x_coords'], df['y_coords']
    g_x, g_y = goal_position

    df['shot_distance'] = np.sqrt((x - g_x) ** 2 + (y - g_y) ** 2)
    return df


def append_shot_angle(df: pd.DataFrame, goal_position=(89, 0)) -> pd.DataFrame:
    """
    function that takes a row of a dataframe and appends the shot to goal angle
    in degrees
    """

    df = df.copy(deep=True)

    x, y = df['x_coords'], df['y_coords']
    g_x, g_y = goal_position

    df['shot_angle'] = np.degrees(np.arctan(abs(x - g_x) / abs(y - g_x)))

    return df


cols_replace = ['goal', 'empty net', 'strength_even', 'strength_shorthand', 'strength_powerplay']
def replace_nan_by(df: pd.DataFrame, columns=cols_replace, fill_value=0) -> pd.DataFrame:
    df.loc[:, columns] = df[columns].fillna(fill_value)
    return df
