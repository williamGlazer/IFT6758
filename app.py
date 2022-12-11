"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app

gunicorn can be installed via:

    $ pip install gunicorn

"""
import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort, session
from flask_session import Session
import redis
import sklearn
import pandas as pd
import joblib
import pickle


import ift6758


LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")

MODEL_DIR = "ift6758/data/models"
DEF_MODEL = f"{MODEL_DIR}/default.pkl"

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

_model = None
_features = []


def _load_model(model_fn):
    """
    Charge un estimateur sklearn.base.BaseEstimator entraîné et sérialisé avec Pickle.
    """

    with open(model_fn, 'rb') as f:
        model = pickle.load(f)
        feats = model.feature_names_in_
        session['model'] = model
        session['feats'] = feats
        app.logger.info(f"Loaded model from {model_fn}: {model}")
    
    # ~ f = open(model_fn, 'rb')
    # ~ _model = pickle.load(f)
    # ~ _features = _model.feature_names_in_
    # ~ app.logger.info(f"Loaded model from {model_fn}: {_model}")


@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e._ load model,
    setup logging handler, etc.)
    """
    # TODO: setup basic logging configuration
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

    _load_model(DEF_MODEL)

@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    
    # TODO: read the log file specified and return the data
    raise NotImplementedError("TODO: implement this endpoint")

    response = None
    return jsonify(response)  # response must be json serializable!


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Recommend (but not required) json with the schema:

        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }
    
    """
    # Get POST json data
    json = request.get_json()
    app.logger.info(json)

    # TODO: check to see if the model you are querying for is already downloaded

    # TODO: if yes, load that model and write to the log about the model change.  
    # eg: app.logger.info(<LOG STRING>)
    
    # TODO: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the 
    # currently loaded model

    # Tip: you can implement a "CometMLClient" similar to your App client to abstract all of this
    # logic and querying of the CometML servers away to keep it clean here

    raise NotImplementedError("TODO: implement this endpoint")

    response = None

    app.logger.info(response)
    return jsonify(response)  # response must be json serializable!


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions
    """

    model = session["model"]
    feats = session["feats"]
    json = request.get_json()
    app.logger.info(json)
    df = pd.read_json(json)
    df2 = df[feats]
    pred = model.predict_proba(df2)
    for i, c in enumerate(model.classes_):
        f = str(c) + "_proba"
        df[f] = pred[:, i]
    return jsonify(df.to_json())  # response must be json serializable!
