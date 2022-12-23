import shutil
import warnings
from logging.config import dictConfig
from pathlib import Path

import sklearn
from comet_ml import API
from flask import Flask, jsonify, request, Response
import json
import os
import pandas as pd
import pickle

LOG_FILE = os.environ.get("FLASK_LOG", "../flask.log")

MODEL_DIR = "../data/models"
DEFAULT_MODEL = f"{MODEL_DIR}/default.pkl"

COMET_NAMESPACE = "williamglazer"
COMET_PROJECT = "hockeyanalysis"

# sets loggers
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "terminal_logger": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file_logger": {
                "filename": LOG_FILE,
                "class": "logging.FileHandler",
                "mode": "a",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["terminal_logger", "file_logger"]},
    }
)

app = Flask(__name__)

# suppress sklearn UserWarning when de-pickling adaboost
warnings.filterwarnings("ignore", category=UserWarning)

app.logger.info("server is up!")


"""
APP FUNCTIONNALITY:

the server stores pickled sklearn files within ../data/models/
upon /predict request, loads the file named default.pkl and outputs a prediction probability
to switch the model, if the file is not found on disk, it is fetched from the web
"""


def get_model() -> sklearn.base.BaseEstimator:
    """gets default pickled sklearn.base.BaseEstimator model"""
    if not Path(DEFAULT_MODEL).exists():
        api = API()
        api.download_registry_model(
            "williamglazer",
            "naive-bayes",
            "1.0.0",
            output_path=f"{MODEL_DIR}/staging/",
            expand=True,
        )
        files = os.listdir(f"{MODEL_DIR}/staging/")
        assert len(files) == 1
        shutil.move(
            f"{MODEL_DIR}/staging/{files[0]}",
            MODEL_DIR + "/williamglazer-naive-bayes-1.0.0.pkl",
        )
        set_model(MODEL_DIR + "/williamglazer-naive-bayes-1.0.0.pkl")

    with open(DEFAULT_MODEL, "rb") as f:
        app.logger.info(f"fetching model from {DEFAULT_MODEL}: ")
        model = pickle.load(f)
        app.logger.info(f"successfully loaded")

    return model


def set_model(path: str):
    """sets default model"""
    app.logger.info(f"setting default model to {path}")
    return shutil.copyfile(path, DEFAULT_MODEL)


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    with open(LOG_FILE, "r") as f:
        logs = f.read()
    return Response(logs, mimetype="text/plain")


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Schéma JSON :
        {
            workspace: (required),
            model: (required),
            version: (required)
        }

    """

    json_str = request.get_json()
    data = json.loads(json_str)

    model_name = f"{data['workspace']}-{data['model']}-{data['version']}.pkl"
    model_path = f"{MODEL_DIR}/{model_name}"

    try:

        if os.path.isfile(model_path):
            app.logger.info(f"model {model_name} already exists")
            set_model(f"{MODEL_DIR}/{model_name}")

        else:
            app.logger.info(f"downloading model {model_name} to {MODEL_DIR}/staging")
            api = API()
            api.download_registry_model(
                data["workspace"],
                data["model"],
                data["version"],
                output_path=f"{MODEL_DIR}/staging",
                expand=True,
            )
            app.logger.info(f"done!")

            files = os.listdir(f"{MODEL_DIR}/staging/")
            assert len(files) == 1
            shutil.move(f"{MODEL_DIR}/staging/{files[0]}", f"{MODEL_DIR}/{model_name}")
            set_model(f"{MODEL_DIR}/{model_name}")

        return jsonify(success=True)

    except Exception as e:
        app.logger.error(f"error loading model: {e}")
        return jsonify(success=False)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Reçoit un DataFrame Pandas sérialisé en JSON,
    Renvoie le même DataFrame avec une colonne de probabilité par classe
    """
    model = get_model()
    model_features = model.feature_names_in_

    dict_data = request.get_json()
    df = pd.DataFrame.from_records(dict_data)
    df_filtered = df[model_features]

    app.logger.info("predicting goal probabilities")

    pred = model.predict_proba(df_filtered)
    response = {"goal_proba": pred[:, 1].tolist()}  # get proba of class 1

    app.logger.info("done!")

    return jsonify(response)
