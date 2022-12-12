"""
Pour tester l'application Flask :

  1. jupyter notebook notebooks/test-flask.ipynb &
  2. redis-server &
  3. gunicorn --bind 127.0.0.1:5000 app:app

"""

from comet_ml import API
from flask import Flask, jsonify, request, abort, session
from flask_session import Session
import json
import logging
import os
import pandas as pd
from pathlib import Path
import pickle
import re

LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")

# Attention : le modèle par défaut doit être présent dès le démarrage
MODEL_DIR = "ift6758/data/models"
DEF_MODEL = f"{MODEL_DIR}/default.pkl"

COMET_NAMESPACE = "williamglazer"
COMET_PROJECT   = "hockeyanalysis"


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)


def _load_model(model_fn):
    """
    Charge un estimateur sklearn.base.BaseEstimator entraîné et sérialisé avec Pickle.
    """

    with open(model_fn, 'rb') as f:
        model = pickle.load(f)
        feats = model.feature_names_in_
        session['model'] = model
        session['feats'] = feats
        app.logger.info(f"Modèle chargé depuis {model_fn}: {model}")


@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e._ load model,
    setup logging handler, etc.)
    """
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    _load_model(DEF_MODEL)


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response""" 
    mesgs = []
    with open(LOG_FILE, 'r') as f:
        # nous allons itérer sur les lignes parce qu'une entrée de log
        # peut faire plusieurs lignes
        tampon = ""
        niveau = None
        app    = None
        for l in f:
            m = re.search(r"([A-Z]+):(\w+):(.*)", l)
            if m:   # nouvelle entrée qui commence
                if niveau:
                    mesgs.append({ "niveau": niveau, "app": app, "message": tampon })
                niveau = m.group(1)
                app    = m.group(2)
                tampon = m.group(3)
            else:   # entrée qui se continue
                tampon = tampon + l
    return jsonify(mesgs)


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
    app.logger.info(json_str)
    data = json.loads(json_str)
    try:
        api = API()
        experiment = api.get(f"{data['workspace']}/{data['project']}/{data['experiment']}")
        model_fn = experiment.get_model_asset_list(data['model'])[0]["fileName"]
        qual_fn = f"{MODEL_DIR}/{model_fn}"
        if os.path.isfile(qual_fn):
            app.logger.info("Le modèle existe déjà")
            _load_model(qual_fn)
        else:
            experiment.download_model(data['model'], output_path=MODEL_DIR, expand=True)
            app.logger.info("Le modèle a été téléchargé")
            _load_model(qual_fn)
        response = "OK"
    except Exception as e:
        app.logger.error(f"Impossible de charger le modèle demandé: {e}")
        response = "Erreur"
    return jsonify(response)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Reçoit un DataFrame Pandas sérialisé en JSON,
    Renvoie le même DataFrame avec une colonne de probabilité par classe
    """
    model = session.get("model")
    feats = session.get("feats")
    json = request.get_json()
    app.logger.info(json)
    df = pd.read_json(json)
    df2 = df[feats] # un DataFrame avec juste les caractéristiques requises par le modèle
    pred = model.predict_proba(df2)
    # ajouter une colonne par classe
    for i, c in enumerate(model.classes_):
        f = str(c) + "_proba"
        df[f] = pred[:, i]
    return jsonify(df.to_json())
