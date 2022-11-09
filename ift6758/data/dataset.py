from pathlib import Path

import pandas as pd
from .features import mirror_coordinates, append_shot_angle, append_shot_distance, replace_nan_by

YEARS = [
    20162017,
    20172018,
    20182019,
    20192020,
    20202021,
    20212022,
]

DEFAULT_TRANSFORMATIONS = (mirror_coordinates, append_shot_angle, append_shot_distance, replace_nan_by)


class Dataset:
    """
    class which will:
    1. load the tabular dataset
    2. transform it with the defined preprocessing operations
    """
    def __init__(
        self,
        tabular_dir: str,
        transformations=DEFAULT_TRANSFORMATIONS
    ):
        self.path = Path(tabular_dir)
        assert self.path.is_dir()
        self.transformations = transformations
        self.df = self._get_dataframe()

    def _get_dataframe(self) -> pd.DataFrame:
        df_list = []

        for season in YEARS:
            df = pd.read_csv(self.path / f'{season}.csv')
            df['season'] = season
            df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)
        return df

    def preprocess(self) -> pd.DataFrame:
        for operation in self.transformations:
            self.df = operation(self.df)
        return self.df
