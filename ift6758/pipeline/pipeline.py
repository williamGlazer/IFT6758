import pickle
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from comet_ml import API, Experiment

from ift6758.pipeline.features import (
    mirror_coordinates,
    append_shot_angle,
    append_shot_distance,
    replace_nan_by_0,
    append_game_secs,
    append_time_lapse_prev,
    append_rebound,
    append_dist_prev,
    append_angle_change,
    append_speed,
    replace_nan_by_0_2,
)
from ift6758.pipeline.plots import (
    plot_roc,
    plot_goal_rate,
    plot_goal_cumsum,
    plot_calibration,
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
    append_game_secs,
    append_time_lapse_prev,
    append_dist_prev,
    append_rebound,
    append_angle_change,
    append_speed,
    replace_nan_by_0_2,
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
        valid_season=20202021,
        random_state=42,
        n_folds_cv=5,
        enable_comet=False,
        model_save_directory="../data/models",
    ):
        if enable_comet:
            API().get()  # throws error if invalid comet api key
        self.enable_comet = enable_comet

        self.random_state = random_state
        self.tabular_dir = tabular_dir
        self.transformations = dataset_transformations
        self.test_season = test_season
        self.valid_season = valid_season
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

        self.model_save_directory = Path(model_save_directory)
        assert self.model_save_directory.is_dir()

    @classmethod
    def get_data(
        cls, tabular_dir: str, transformations: list[callable]
    ) -> pd.DataFrame:
        df_list = []

        path = Path(tabular_dir)
        assert path.is_dir()

        print(f"fetching dataframes from {path}")
        for season in YEARS:
            df = pd.read_csv(path / f"{season}.csv")
            df["season"] = season
            df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)

        for operation in transformations:
            print(f"applying {operation.__name__}")
            df = operation(df)
        print("done with preprocessing")

        return df

    def run(self):
        np.random.seed(self.random_state)

        df = ExperimentPipeline.get_data(self.tabular_dir, self.transformations)
        x_train, y_train, x_valid, y_valid, x_test, y_test = self._split_train_test(df)
        self.grid.fit(x_train, y_train)

        if self.enable_comet:
            self._log_to_comet()

    def _preprocess(self) -> pd.DataFrame:
        for operation in self.transformations:
            self.df = operation(self.df)
        return self.df

    def _split_train_test(
        self, df: pd.DataFrame
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
    ]:
        is_valid = df["season"] == self.valid_season
        is_test = df["season"] == self.test_season

        x_train = df.loc[~is_test & ~is_valid, self.feature_columns]
        y_train = df.loc[~is_test & ~is_valid, self.target_column]
        x_valid = df.loc[is_valid, self.feature_columns]
        y_valid = df.loc[is_valid, self.target_column]
        x_test = df.loc[is_test, self.feature_columns]
        y_test = df.loc[is_test, self.target_column]

        self.dataset = {
            "x_train": x_train,
            "y_train": y_train,
            "x_valid": x_valid,
            "y_valid": y_valid,
            "x_test": x_test,
            "y_test": y_test,
        }

        return x_train, y_train, x_valid, y_valid, x_test, y_test

    def get_probas(self, dataset: str):
        assert dataset in ["train", "valid", "test"]
        return self.grid.best_estimator_.predict_proba(self.dataset[f"x_{dataset}"])[
            :, 1
        ]

    def get_preds(self, dataset: str):
        assert dataset in ["train", "valid", "test"]
        return self.grid.best_estimator_.predict(self.dataset[f"x_{dataset}"])

    def get_metrics(self, dataset: str):
        assert dataset in ["train", "valid", "test"]

        truth = self.dataset[f"y_{dataset}"]
        preds = self.get_preds(dataset)
        probas = self.get_probas(dataset)

        accuracy = accuracy_score(truth, preds)
        f1 = f1_score(truth, preds)
        roc_auc = roc_auc_score(truth, probas)

        return {"accuracy": accuracy, "f1": f1, "roc_auc": roc_auc}

    def _log_to_comet(self):
        exp = Experiment(
            project_name="hockeyanalysis",
        )

        # parameters
        exp.log_parameter(
            name="dataset_transformations",
            value=str([fn.__name__ for fn in self.transformations]),
        )
        exp.log_parameter(name="features", value=str(self.feature_columns))
        exp.log_parameter(name="parameter_grid", value=str(self.grid.param_grid))
        exp.log_parameter(name="best_parameters", value=str(self.grid.best_params_))

        # metrics
        metrics = self.get_metrics("valid")
        exp.log_metric(name="best_model_valid_accuracy", value=metrics["accuracy"])
        exp.log_metric(name="best_model_valid_f1", value=metrics["f1"])
        exp.log_metric(name="best_model_valid_roc_auc", value=metrics["roc_auc"])

        # best model
        filepath = self._generate_model_filepath()
        self._save_model(filepath)
        exp.log_model(name="best_model", file_or_folder=filepath)

        # plots
        (
            roc_plot,
            goal_rate_plot,
            goal_cumsum_plot,
            calibration_plot,
        ) = self._get_figures()

        exp.log_figure(figure_name="roc", figure=roc_plot)
        exp.log_figure(figure_name="goal_rate", figure=goal_rate_plot)
        exp.log_figure(figure_name="goal_cumsum", figure=goal_cumsum_plot)
        exp.log_figure(figure_name="", figure=calibration_plot)

        exp.end()

    def _generate_model_filepath(self) -> str:
        timestamp = str(datetime.now())
        model_name = str(self.grid.best_estimator_)

        filename = f"{model_name}-{timestamp}.pkl"
        return str(self.model_save_directory / filename)

    def _save_model(self, path: str):
        best_model = self.grid.best_estimator_
        with open(path, "wb") as file:
            pickle.dump(best_model, file)

    def _get_figures(self):
        truth = self.dataset["y_valid"]
        probas = self.get_probas("valid")
        preds = self.get_preds("valid")

        roc_plot = plot_roc([truth], [probas], [preds])
        goal_rate_plot = plot_goal_rate([truth], [probas], [preds])
        goal_cumsum_plot = plot_goal_cumsum([truth], [probas], [preds])
        calibration_plot = plot_calibration([truth], [probas], [preds])

        return roc_plot, goal_rate_plot, goal_cumsum_plot, calibration_plot
