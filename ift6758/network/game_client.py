import functools
from typing import Any

import pandas as pd

from ..data.extractor import NHLExtractor
from ..data.cleaner import NHLCleaner
from ..pipeline.pipeline import DEFAULT_TRANSFORMATIONS


class GameClient:
    @staticmethod
    def get_game_data(game_id: int) -> pd.DataFrame:
        raw = NHLExtractor().get_game_data(game_id)

        clean = NHLCleaner.format_game(raw)

        def chain(data: Any, functions: list[callable]) -> Any:
            for f in functions:
                data = f(data)
            return data

        df = pd.DataFrame(clean)
        processed = chain(df, DEFAULT_TRANSFORMATIONS)

        return processed