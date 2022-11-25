---
layout: post
title: Téléchargement de Données
---

Éxécuter le notebook `notebooks/data_extraction.ipynb` qui fait les actions suivantes:
1. télécharge les données brutes à `../data/raw/[YEARYEAR].json` sous format .JSON
2. nettoie les données et sauvegarde sous `../data/tabular/` en format csv.

Voici le code exécuté par le notebook:
```Python
from ift6758 import NHLLoader, NHCleaner

# Either download from API or extracted data from GDrive
NHLLoader.from_api(out_dir='../data/raw/')
# OR
NHLLoader.from_gdrive(out_dir="../data/raw/")

for season in [
    20162017,
    20172018,
    ...
]:
    df = NHLCleaner.format_season(f'../data/raw/{season}.json')
    df.to_csv(f'../data/tabular/{season}.csv', index=False)
```

Nous avons ajouté une méthode pour télécharger les données directement de GDrive afin de ne pas spam l'API de la LNH.

Si vous ne voulez pas télécharger notre code python et l'installer en tant que package, vous pouvez aussi consulter le code source dans notre répertoire GitHub.