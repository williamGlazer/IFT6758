import pandas as pd

from ..data.extractor import NHLExtractor
from ..data.cleaner import NHLCleaner

class GameClient:

    @staticmethod
    def get_game_data(id: int) -> pd.DataFrame:
        # store results in cache
        data = NHLExtractor.get_game_data(id)
        # format using NHLCleaner => needs to refactor to use for single game
        # preprocess using pipeline functions
        # return result
        pass


