from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from comet_ml import API

from ift6758.pipeline.features import (
    mirror_coordinates,
    append_shot_angle,
    append_shot_distance,
    replace_nan_by_0,
)

YEARS = [
    20162017,
    20172018,
    20182019,
    20192020,
    20202021,
    20212022,
]

DEFAULT_TRANSFORMATIONS = (
    mirror_coordinates,
    append_shot_angle,
    append_shot_distance,
    replace_nan_by_0,
)


class ExperimentPipeline:
    def __init__(
        self,
        feature_columns: list[str],
        target_column: str,
        pipeline_steps: list,
        tabular_dir: str,
        metric: str,
        dataset_transformations: list[callable] = DEFAULT_TRANSFORMATIONS,
        parameter_grid=list[dict],
        test_season=20212022,
        random_state=42,
        n_folds_cv=5,
        enable_comet=False,
    ):
        if enable_comet:
            API().get() # throws error if invalid comet api key
        self.enable_comet = enable_comet

        self.random_state = random_state
        self.tabular_dir = tabular_dir
        self.transformations = dataset_transformations
        self.test_season = test_season
        self.feature_columns = feature_columns
        self.target_column = target_column

        self.pipeline = Pipeline(pipeline_steps)
        self.grid = GridSearchCV(
            self.pipeline,
            parameter_grid,
            cv=n_folds_cv,
            scoring=metric,
            verbose=3,
        )
        self.dataset = None

    @classmethod
    def get_data(
        cls, tabular_dir: str, transformations: list[callable]
    ) -> pd.DataFrame:
        df_list = []

        path = Path(tabular_dir)
        assert path.is_dir()

        print(f'fetching dataframes from {path}')
        for season in YEARS:
            df = pd.read_csv(path / f"{season}.csv")
            df["season"] = season
            df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)

        for operation in transformations:
            print(f'applying {operation.__name__}')
            df = operation(df)

        return df

    def run(self):
        np.random.seed(self.random_state)

        df = ExperimentPipeline.get_data(self.tabular_dir, self.transformations)
        x_train, y_train, x_test, y_test = self._split_train_test(df)
        self.grid.fit(x_train, y_train)

        if self.enable_comet:
            self._log_to_comet()

    def _preprocess(self) -> pd.DataFrame:
        for operation in self.transformations:
            self.df = operation(self.df)
        return self.df

    def _split_train_test(
        self, df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        is_test = df["season"] == self.test_season

        x_train = df.loc[~is_test, self.feature_columns]
        y_train = df.loc[~is_test, self.target_column]
        x_test = df.loc[is_test, self.feature_columns]
        y_test = df.loc[is_test, self.target_column]

        self.dataset = {
            'x_train': x_train,
            'y_train': y_train,
            'x_test': x_test,
            'y_test': y_test
        }

        return x_train, y_train, x_test, y_test

    def get_test_probas(self):
        return self.grid.best_estimator_.predict_proba(self.dataset['x_test'])

    def _log_to_comet(self):
        # taken from https://www.comet.com/docs/v2/integrations/ml-frameworks/scikit-learn/
        # TODO log features, target, pipeline
        # TODO should we log test acc to Comet?
        # TODO prettify results
        # for i in ...:
        #     exp = Experiment(
        #         project_name="hockeyanalysis",
        #     )
        #     exp.log_parameters(...)
        #     exp.log_metric(..., ...)
        #     exp.end()
        pass
