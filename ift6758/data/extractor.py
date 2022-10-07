from enum import Enum
from typing import List

import requests
from tqdm import tqdm


class GameType(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALL_STAR = 4

DEFAULT_GAME_TYPES = [GameType.REGULAR, GameType.PLAYOFFS]

OK = 200
NOT_FOUND = 404


class NHLExtractor:
    """
    Class to interface the API of the NHL statistics
    """

    def __init__(self, game_types: List[GameType] = DEFAULT_GAME_TYPES):
        self.game_types = game_types
        self.game_url = "https://statsapi.web.nhl.com/api/v1/game/{}/feed/live/"
        self.schedule_url = "https://statsapi.web.nhl.com/api/v1/schedule?season={}"

    def get_season_data(self, season: int) -> List[dict]:
        print(f"getting season {season} game ids")
        game_ids = self.get_game_ids(season)

        print("getting game data")
        season_data = [
            self.get_game_data(id)
            for id in tqdm(game_ids)
            if self._get_type_from_id(id) in self.game_types
        ]
        return season_data

    def get_game_ids(self, season: int) -> List[int]:
        assert len(str(season)) == 8, f"{season} need to be: [Ystart][Yend]"

        season_url = self.schedule_url.format(season)
        data = self._get_data_from(season_url)

        ids = []
        for date_games in data["dates"]:
            for game in date_games["games"]:
                ids.append(
                    game["gamePk"]
                )

        return ids

    def get_game_data(self, game_id: int) -> dict:
        game_url = self.game_url.format(game_id)
        return self._get_data_from(game_url)

    def _get_type_from_id(self, id: int) -> GameType:
        type = int(str(id)[5])
        return GameType(type)

    def _get_data_from(self, url: str) -> dict:
        response = requests.get(url)

        if response.status_code == OK:
            return response.json()
        elif response.status_code == NOT_FOUND:
            raise LookupError(f"not found at url {response.url}")
        else:
            raise Exception(f"unknown error {response.status_code} at url {response.url}")
