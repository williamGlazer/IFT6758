import itertools

import pandas as pd
import json
import os

COLUMNS = [
    "game starttime",
    "game endtime",
    "gameId",
    "datetime",
    "offense_team_id",
    "offense_team_name",
    "offense_team_tricode",
    "goal",
    "x_coords",
    "y_coords",
    "period",
    "period_time",
    "goalie_id",
    "goalie_name",
    "shooter_id",
    "shooter_name",
    "shot type",
    "prev_type",
    "prev_x_coords",
    "prev_y_coords",
    "prev_datetime",
    "empty net",
    "strength_shorthand",
    "strength_even",
    "strength_powerplay"

]


class NHLCleaner:
    """
    Class to convert data from raw json to interpretable table with following constraints
    "all events of every game into a pandas dataframe, include events of the type “shots” and “goals”, ignore missed shots or blocked shots for now"
    Features :
        - game time/period information,
        - game ID, team information (which team took the shot),
        - indicator if its a shot or a goal,
        - the on-ice coordinates,
        - the shooter
        - goalie name (don’t worry about assists for now),
        - shot type,
        - if it was on an empty net
        - whether or not a goal was at even strength, shorthanded, or on the power play
    """

    # liveData/plays/
    def __init__(self) -> None:
        pass

    @staticmethod
    def _pull_json(path: str) -> dict:
        with open(path) as f:
            data = json.load(f)

        if not data:
            raise FileNotFoundError(f"file not found at {path}")

        return data
    @staticmethod
    def _is_invalid_game_data(game: dict) -> bool:
        # 1 gamePk was 12 and not in [01, 02, 03, 04]
        is_invalid_id = str(game["gamePk"])[4] != '0'

        # 1 game data had no endDateTime field
        is_invalid_start = "endDateTime" not in game["gameData"]["datetime"]

        return is_invalid_id or is_invalid_start

    @staticmethod
    def format_season(path: str) -> pd.DataFrame:
        try:                                                                           
            raw_data = NHLCleaner._pull_json(path)
        except UnicodeDecodeError as error:  # includes JSONDecodeError                          
            print(f'{path} not JSON')                                                       
            return pd.DataFrame()

        nested_tabular_data: list[list[dict]] = [
            NHLCleaner.format_game(game)
            for game in raw_data
            if not NHLCleaner._is_invalid_game_data(game)
        ]

        # unpacks the list of dicts
        tabular_data: list[dict] = list(itertools.chain.from_iterable(nested_tabular_data))

        return pd.DataFrame(tabular_data)


    @staticmethod
    def format_game(game: dict) -> list[dict]:
        events = []

        event_list = game["liveData"]["plays"]["allPlays"]

        for eventIdx in range(len(event_list)):
            event = game["liveData"]["plays"]["allPlays"][eventIdx]

            if (
                event["result"]["event"] == "Shot"
                or event["result"]["event"] == "Goal"
            ):
                curr_event = {}

                curr_event["game_starttime"] = game["gameData"]["datetime"]["dateTime"]
                curr_event["game_endtime"] = game["gameData"]["datetime"]["endDateTime"]
                curr_event["game_id"] = game["gamePk"]

                curr_event["datetime"] = event['about']['dateTime']
                curr_event["offense_team_id"] = event["team"]["id"]
                curr_event["offense_team_name"] = event["team"]["name"]
                curr_event["offense_team_tricode"] = event["team"]["triCode"]
                curr_event["goal"] = (0 if event["result"]["event"] == "Shot" else 1)
                curr_event["x_coords"] = event["coordinates"].get("x", None)
                curr_event["y_coords"] = event["coordinates"].get("y", None)
                curr_event["period"] = event['about']['period']
                curr_event["period_time"] = event['about']['periodTime']

                for p in event["players"]:
                    if p["playerType"] == "Goalie":
                        curr_event["goalie_id"] = p["player"]["id"]
                        curr_event["goalie_name"] = p["player"]["fullName"]

                for p in event["players"]:
                    if p["playerType"] == "Shooter" or p["playerType"] == "Scorer":
                        curr_event["shooter_id"] = p["player"]["id"]
                        curr_event["shooter_name"] = p["player"]["fullName"]

                curr_event["shot_type"] = event["result"].get("secondaryType", None)

                ## Info Event Precedent
                prev_event = game["liveData"]["plays"]["allPlays"][eventIdx-1]
                curr_event["prev_type"] = prev_event["result"]["event"]
                curr_event["prev_x_coords"] = prev_event["coordinates"].get("x", None)
                curr_event["prev_y_coords"] = prev_event["coordinates"].get("y", None)
                curr_event["prev_datetime"] = prev_event['about']['dateTime']

                if event["result"]["event"] == "Goal":
                    curr_event["empty_net"] = event["result"].get("emptyNet", None)
                    ##
                    if event["result"]["strength"].get("code", None) == "EVEN":
                        curr_event["strength_shorthand"] = 0
                        curr_event["strength_even"] = 1
                        curr_event["strength_powerplay"] = 0
                    elif event["result"]["strength"].get("code", None) == "PPG":
                        curr_event["strength_shorthand"] = 0
                        curr_event["strength_even"] = 0
                        curr_event["strength_powerplay"] = 1
                    else:
                        curr_event["strength_shorthand"] = 1
                        curr_event["strength_even"] = 0
                        curr_event["strength_powerplay"] = 0
                else:
                    curr_event["empty_net"] = False
                    curr_event["strength_shorthand"] = None
                    curr_event["strength_even"] = None
                    curr_event["strength_powerplay"] = None

                events.append(curr_event)

        return events

        
    @staticmethod
    def format_folder(in_dir:str, out_dir:str) -> None:
        for fn in os.listdir(in_dir):
            in_path = os.path.join(in_dir, fn)
            
            if os.path.isfile(in_path):
                print(in_dir+fn)
                df = NHLCleaner.format_season(in_dir+fn)

                if df is None: continue
                df.to_csv(path_or_buf=os.path.join(out_dir, fn[:-5]+'.csv'), index=False)

        print("done!")