import json
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 8080):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.

        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """
        data = X.to_json()
        serialized_data = json.loads(data)
        response = requests.post(
            f'{self.base_url}/predict',
            json=serialized_data
        )
        body = response.json()
        df = pd.DataFrame.from_records(body)
        return df

    def logs(self) -> str:
        """Get server logs"""
        response = requests.get(
            f'{self.base_url}/logs'
        )
        return response.json()

    def download_registry_model(self, workspace: str, model: str, version: str) -> int:
        """
        Triggers a "model swap" in the service; the workspace, model, and model version are
        specified and the service looks for this model in the model registry and tries to
        download it.
        See more here:
            https://www.comet.ml/docs/python-sdk/API/#apidownload_registry_model

        Args:
            workspace (str): The Comet ML workspace
            model (str): The model in the Comet ML registry to download
            version (str): The model version to download
        """
        data = {
            "workspace": workspace,
            "model": model,
            "version": version,
        }
        serialized_data = json.dumps(data)
        response = requests.post(
            f"{self.base_url}/download_registry_model",
            json=serialized_data
        )

        return response.json()
