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
        dataset_partition=None,
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
        self.dataset_partition = dataset_partition

        self.model_save_directory = Path(model_save_directory)
        assert self.model_save_directory.is_dir()

    @classmethod
    def get_data(
        cls, tabular_dir: str, transformations: list[callable],
        reg=True, playoffs=False, years=YEARS
    ) -> pd.DataFrame:
        df_list = []

        path = Path(tabular_dir)
        assert path.is_dir()

        print(f"fetching dataframes from {path}")
        for season in years:
            df = pd.read_csv(path / f"{season}.csv")
            df["season"] = season
            df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)

        for operation in transformations:
            print(f"applying {operation.__name__}")
            df = operation(df)
        print("done with preprocessing")
        idx = None
        if reg and playoffs: 
            idx = df.index[(df['game_id']//10000%10 == 2) + (df['game_id']//10000%10 == 3)]
        elif reg:
            idx = df.index[df['game_id']//10000%10 == 2]
        elif playoffs:
            idx = df.index[df['game_id']//10000%10 == 3]
            
        return df.loc[idx]

    def run(self):
        np.random.seed(self.random_state)

        if self.enable_comet:
            self.experiment = Experiment(
                project_name="hockeyanalysis",
            )

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
        is_test = df["season"] == self.test_season

        if self.dataset_partition == 'stratify':
            is_valid = (df.index % 5 == 0) & ~is_test
        else:
            is_valid = df['season'] == self.valid_season

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
        # parameters
        self.experiment.log_parameter(
            name="dataset_transformations",
            value=str([fn.__name__ for fn in self.transformations]),
        )
        self.experiment.log_parameter(name="features", value=str(self.feature_columns))
        self.experiment.log_parameter(name="parameter_grid", value=str(self.grid.param_grid))
        self.experiment.log_parameter(name="best_parameters", value=str(self.grid.best_params_))

        # metrics
        metrics = self.get_metrics("valid")
        self.experiment.log_metric(name="best_model_valid_accuracy", value=metrics["accuracy"])
        self.experiment.log_metric(name="best_model_valid_f1", value=metrics["f1"])
        self.experiment.log_metric(name="best_model_valid_roc_auc", value=metrics["roc_auc"])

        # best model
        filepath = self._generate_model_filepath()
        self._save_model(filepath)
        self.experiment.log_model(name="best_model", file_or_folder=filepath)

        # plots
        (
            roc_plot,
            goal_rate_plot,
            goal_cumsum_plot,
            calibration_plot,
        ) = self._get_figures()

        self.experiment.log_figure(figure_name="roc", figure=roc_plot)
        self.experiment.log_figure(figure_name="goal_rate", figure=goal_rate_plot)
        self.experiment.log_figure(figure_name="goal_cumsum", figure=goal_cumsum_plot)
        self.experiment.log_figure(figure_name="calibration", figure=calibration_plot)

        self.experiment.end()

    def _generate_model_filepath(self) -> str:
        timestamp = str(datetime.now())
        filename = f"model_created_{timestamp}.pkl"
        return str(self.model_save_directory / filename)

    def _save_model(self, path: str):
        best_model = self.grid.best_estimator_
        with open(path, "wb") as file:
            pickle.dump(best_model, file)

    def _get_figures(self, dataset='valid'):
        truth = self.dataset[f"y_{dataset}"]
        probas = self.get_probas(dataset)
        preds = self.get_preds(dataset)

        roc_plot = plot_roc([truth], [probas], [preds])
        goal_rate_plot = plot_goal_rate([truth], [probas], [preds])
        goal_cumsum_plot = plot_goal_cumsum([truth], [probas], [preds])
        calibration_plot = plot_calibration([truth], [probas], [preds])

        return roc_plot, goal_rate_plot, goal_cumsum_plot, calibration_plot
