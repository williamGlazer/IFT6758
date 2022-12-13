## Évaluation Préliminaire

Notre technique d'évaluation s'est résumé en un processus à deux étapes. D'abords, nous essayons plusieurs modèles différents sans ajustage d'hyper-paramètres.

Ceci nous permet de courvrir un large éventail de technique sans trop perdre de temps sur des solution peu prometteuses.

Puis nous conservons les modèles un sont dans un écart de 10% de performance ROC-AUC du meilleur modèle _out-of-the-box_.

| Modèle                          | Comet link                                                                                 | ROC-AUC |
|---------------------------------|--------------------------------------------------------------------------------------------|---------|
 | KNN                             | [url](https://www.comet.com/williamglazer/hockeyanalysis/5a66b7c2394b4e94b35c9d2a5d94c9f6) | .606    |
| Decision Tree                   | [url](https://www.comet.com/williamglazer/hockeyanalysis/6b6ebcf77af64cee9c5454d8d69a6cf2) | .537    |
| Random Forest                   | [url](https://www.comet.com/williamglazer/hockeyanalysis/3d6a8e0df0f34461b11f6e165f8bd4ad) | .692    |
| **AdaBoost**    (best)          | [url](https://www.comet.com/williamglazer/hockeyanalysis/195b09dca5114ec79174f86cd46382de) | .**728**    |
| Naive Bayes                     | [url](https://www.comet.com/williamglazer/hockeyanalysis/6ab70286a4aa42309edfc241d6e63857) | .714    |
| Quadratic Discriminant Analysis | [url](https://www.comet.com/williamglazer/hockeyanalysis/3e15ce4a2f8d423bb3fe22df3efd2a5e) | .714    |
| XGBoost                         | [url](https://www.comet.com/williamglazer/hockeyanalysis/857cdd44f44e4f0b8ab33f4f1014683e) | .720    |

Le meilleur modèle semblait de loin être AdaBoost, nous avons donc élu celui-ci comme le seul

Nos graphiques pour chaque modèle sont enregistré dans Comet.ml sous `assets & Artifacts > images > plots.svg`. Voici un extrait du meilleur modèle AdaBoost et du pire modèle de Decision Tree

| AdaBoost Best Model                                                                                                                   |                                                                                                                                    |
|---------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| ROC ![roc](https://s3.amazonaws.com/comet.ml/image_3e15ce4a2f8d423bb3fe22df3efd2a5e-dE4JTLPcoZzLi87sJttqj4pEb.svg)                    | Goal Rate ![rate](https://s3.amazonaws.com/comet.ml/image_3e15ce4a2f8d423bb3fe22df3efd2a5e-8vspTwsE5myusII0nzSIbtXv6.svg)          |
| Goal Cumulative Sum ![cumsum](https://s3.amazonaws.com/comet.ml/image_3e15ce4a2f8d423bb3fe22df3efd2a5e-HLi2gNqLeVghEDAqcmUJuOXX2.svg) | Calibration ![calibration](https://s3.amazonaws.com/comet.ml/image_3e15ce4a2f8d423bb3fe22df3efd2a5e-CWxEUTep0HUwDRbMCKGblOfvj.svg) |


| Decision Tree Worst Model                                                                                          |                                                                                                                                    |
|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Ces modèle n'a pas de probabilitée                                                                                 ||
| ROC ![roc](https://s3.amazonaws.com/comet.ml/image_6b6ebcf77af64cee9c5454d8d69a6cf2-jv53HKFXDis9tTF638Er5Yq7n.svg) | Calibration ![calibration](https://s3.amazonaws.com/comet.ml/image_6b6ebcf77af64cee9c5454d8d69a6cf2-SFcJYgNvort0c4R8UOUMBBLHH.svg) |

## Recherche d'Hyper Paramètres

[Comet.ml](https://www.comet.com/williamglazer/hockeyanalysis/e653e4860266487eae799e75133fbda7?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=step)

| Parameter              | Values             |
|------------------------|--------------------|
| base learner max depth | [1,2,3]            |
| base learner           | Decision Treee Clf |
| learning rate          | [0.1, 1, 10]       |
| n estimators           | [25, 50, 75]       |

Notre meilleure modèle s'avère être:

```
{
   'adaboost__base_estimator': DecisionTreeClassifier(max_depth=3),
   'adaboost__learning_rate': 0.1,
   'adaboost__n_estimators': 75
}
```

avec un ROC-AUC de **.739** ce qui est une faible augmentation de +.002.

## Stratified Sampling

[Comet.ml](https://www.comet.com/williamglazer/hockeyanalysis/e91356fedb86466fad342357d034a4fe)

Notre dernière tentative est de stratifier nos exemples d'entrainement à travers les années afin d'avoir une meilleur représentation de nos performances

Nos performances n'ont pas augmenté