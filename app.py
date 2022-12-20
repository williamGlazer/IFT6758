import shutil
from logging.config import dictConfig
from pathlib import Path

from comet_ml import API
from flask import Flask, jsonify, request
import json
import os
import pandas as pd
import pickle

LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")
os.environ["COMET_API_KEY"] = "8xjLFJfXYPcxbIanNSTVnZI4O"

MODEL_DIR = "data/models"
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


def get_model():
    """gets default pickled sklearn.base.BaseEstimator model"""
    if not Path(DEFAULT_MODEL).exists():
        api = API()
        experiment = api.get("williamglazer/hockeyanalysis/bfbb2c0cf043468f883b3dd4bf5febd2")
        model_fn = experiment.get_model_asset_list('best_model')[0]["fileName"]
        experiment.download_model('best_model', output_path=MODEL_DIR, expand=True)
        qual_fn = f"{MODEL_DIR}/{model_fn}"
        set_model(qual_fn)

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
        return jsonify(f.read())


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Schéma JSON :
        {
            workspace: (required),
            project: (required),
            experiment: (required),
            model: (required)
        }

    """

    json_str = request.get_json()
    data = json.loads(json_str)

    try:
        api = API()
        experiment = api.get(
            f"{data['workspace']}/{data['project']}/{data['experiment']}"
        )
        model_fn = experiment.get_model_asset_list(data["model"])[0]["fileName"]
        qual_fn = f"{MODEL_DIR}/{model_fn}"

        if os.path.isfile(qual_fn):
            app.logger.info(f"model {data['model']} already exists")
            set_model(qual_fn)

        else:
            app.logger.info(f"downloading model {data['model']} to {MODEL_DIR}")
            experiment.download_model(data["model"], output_path=MODEL_DIR, expand=True)
            app.logger.info(f"done!")
            set_model(qual_fn)

        return jsonify("OK")

    except Exception as e:
        app.logger.error(f"error loading model: {e}")
        return jsonify("ERROR")


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
