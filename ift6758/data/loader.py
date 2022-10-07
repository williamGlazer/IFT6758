import json
import zipfile
from pathlib import Path

import gdown

from ift6758.data.extractor import NHLExtractor

GDRIVE_URL = "https://drive.google.com/uc?id=1Swfx9TAEReBMXkuPwwAR-hHlU1NuAXVt"
SEASONS = [
    20162017,
    20172018,
    20182019,
    20192020,
    20202021,
    20212022,
]

class NHLLoader:
    """
    Abstract class to download file directly form the API or from as stored version on GDrive
    """

    @staticmethod
    def from_gdrive(out_dir: str):
        dir = NHLLoader._get_dir(out_dir)
        zip_file = str(dir/"NHL.zip")

        gdown.download(GDRIVE_URL, zip_file, quiet=False)

        #extract
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dir)

    @staticmethod
    def from_api(out_dir: str):
        dir = NHLLoader._get_dir(out_dir)

        for season in SEASONS:
            file_path = dir/f"{season}.json"
            if file_path.exists():
                continue

            data = NHLExtractor().get_season_data(season)

            with open(file_path, 'w+') as f:
                json.dump(data, f)

    @staticmethod
    def _get_dir(dir: str) -> Path:
        dir = Path(dir).resolve()

        if not dir.is_dir():
            raise NotADirectoryError(f"directory {dir.name} not found")

        return dir
