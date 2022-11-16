"""
Add all transformations from the raw tabular dataset to the preprocessed version here
"""
import pandas as pd
import numpy as np
from datetime import datetime


def mirror_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    function that takes a dataframe and mirrors the shot coordinates
    if the shot is in a negative x coordinate
    """
    df = df.copy(deep=True)
    x, y = df["x_coords"], df["y_coords"]

    is_x_negative = df["x_coords"] < 0

    df.loc[is_x_negative, "x_coords"] = -x
    df.loc[is_x_negative, "y_coords"] = -y

    return df


def append_shot_distance(df: pd.DataFrame, goal_position=(89, 0)) -> pd.DataFrame:
    """
    function that takes a row of a dataframe and appends the shot to goal distance
    in euclidean norm
    """
    df = df.copy(deep=True)

    x, y = df["x_coords"], df["y_coords"]
    g_x, g_y = goal_position

    df["shot_distance"] = np.sqrt((x - g_x) ** 2 + (y - g_y) ** 2)
    return df


def append_shot_angle(df: pd.DataFrame, goal_position=(89, 0)) -> pd.DataFrame:
    """
    function that takes a row of a dataframe and appends the shot to goal angle
    in degrees
    """

    df = df.copy(deep=True)

    x, y = df["x_coords"], df["y_coords"]
    g_x, g_y = goal_position

    df["shot_angle"] = np.degrees(np.arctan(abs(x - g_x) / abs(y - g_y)))

    return df


def append_game_secs(df: pd.DataFrame,) -> pd.DataFrame:
    '''
    function that take the dataframe returns a copy with the game time in seconds
    '''
    df = df.copy(deep=True)
    minutes = df['period_time'].str[:2].astype(int)
    secs = df['period_time'].str[3:].astype(int)
    df['game_secs'] = (df['period']-1)*20*60+minutes*60+secs

    # alternative but doesn't calculate time played, not implemented
    # datetime.strptime(df.loc[0, 'datetime'], '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(df.loc[0, 'game starttime'], '%Y-%m-%dT%H:%M:%SZ')

    return df


def append_time_lapse_prev(df: pd.DataFrame) -> pd.DataFrame:
    '''
    function that take the dataframe returns a copy with time lapsed since previous event
    '''

    df = df.copy(deep=True)
    for idx, row in df.iterrows():
        print(row)
        prev_dt = datetime.strptime(row['prev_datetime'], '%Y-%m-%dT%H:%M:%SZ')
        curr_dt = datetime.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%SZ')
    df['time_lapsed_prev_event'] = curr_dt - prev_dt


### DISTANCE DEPUIS DERNIER EVENT
def append_dist_prev(df: pd.DataFrame) -> pd.DataFrame:
    '''
    function that take the dataframe returns a copy with the distance to previous event
    '''
    df = df.copy(deep=True)

    x, y = df["x_coords"], df["y_coords"]
    prev_x, prev_y = df["prev_x_coords"], df["prev_y_coords"]

    df["dist_prev_event"] = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
    return df


def append_rebound(df: pd.DataFrame) -> pd.DataFrame:
    '''
    function that take the dataframe returns a copy with a bool column indicating whether rebound
    '''
    df = df.copy(deep=True)

    df['rebound'] = (df['prev_type']=="Shot")
    return df


def append_angle_change(df: pd.DataFrame, goal_position=(89, 0)) -> pd.DataFrame:
    '''
    Requires "rebound" column
    function that take the dataframe returns a copy with a column indicating the angle change if previous event was a shot
    else appends none
    '''
    df = df.copy(deep=True)
    for idx, row in df.iterrows():
        if row['rebound']:
            x, y = df["prev_x_coords"], df["prev_y_coords"]
            g_x, g_y = goal_position

            prev_shot_angle = np.degrees(np.arctan(abs(x - g_x) / abs(y - g_y)))

            df.loc[idx,'angle_change'] = df['shot_angle'] - prev_shot_angle
        else:
            df.loc[idx,'angle_change'] = None
    
    return df 


def append_speed(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Requires: 'dist_previous_events', 'time_lapsed_prev_event'
    function that take the dataframe returns a copy with the speed between shot and previous event
    '''
    df = df.copy(deep=True)
    df['speed'] = df['dist_prev_event'] / df['time_lapsed_prev_event']
    
    return df    


cols_replace = [
    "goal",
    "empty_net",
    "strength_even",
    "strength_shorthand",
    "strength_powerplay",
    "shot_distance",
    "shot_angle",
]


def replace_nan_by_0(
    df: pd.DataFrame, columns=cols_replace, fill_value=0
) -> pd.DataFrame:
    df.loc[:, columns] = df[columns].fillna(fill_value)
    return df
