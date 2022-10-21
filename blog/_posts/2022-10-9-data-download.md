---
layout: post
title: Download the Data, tutoriel
---

```
Rédigez un bref tutoriel sur la façon dont votre équipe a téléchargé l’ensemble de données. Imaginez :) que vous cherchiez un guide sur la façon de télécharger les données play-by-play ; votre guide devrait vous faire dire “Parfait - c’est exactement ce que je cherchais!”. Inclure votre fonction/classe et un exemple de comment l’utiliser.
```

Executer le notebook `notebooks/data_extraction.ipynb`:

Telechargera les données brutes à `../data/raw/[YEARYEAR].json` sous format JSON
Telechargera les données nettoyées seront dossier `../data/tabular/` sous format csv. Il suffit ensuite de lire le csv local pour les précédures suivantes.
Ce notebook utilise le package construit dans `ift6758/data`, contenant les classes suivantes:

- NHLExtractor
- NHLLoader
- NHLCleaner
Deux méthodes sont disponibles pour téléchargées à partir de NHLLoader, les données brutes: directement de l’API ou par gdrive. Le contient les 2 methodes, l’une commentée.