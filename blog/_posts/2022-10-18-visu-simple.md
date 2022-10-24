---
layout: post
title: Visualisations simples
---

Visualisations simples
======================

Types de tir
------------

Dans le respect des consignes, qui exigeaient de superposer le nombre de tirs et le nombre de buts de chaque type, nous avons réalisé un diagramme à barres empilées où chaque barre représente un type de tir. Cependant, ce n'est pas nécessairement la visualisation idéale pour répondre à toutes les questions ici.

![Histogramme des tirs et buts en fonction du type de tir (saison 2016-2017)](figures/q5-1.png)

Si on constate aisément que le «wrist shot» est le type le plus courant, suivi loin derrière par les «slap shots» et les «snap shots», le diagramme donne par contre l'impression que les «wrist shots» et les «snap shots» sont particulièrement redoutables, alors que nos données indiquent que ce ne sont pas les types de tir qui se traduisent proportionnellement par le plus de buts.

Une visualisation combinant, par exemple, une barre représentant le nombre de tirs de chaque type accompagné d'une ligne représentant la *proportion* de ces tirs résultant en un but aurait été plus parlante, et aurait par exemple révélé que les types de tir les plus redoutables sont «deflected» et «tip-in».

Distance de tir
---------------

Pour cette question, nous avons choisi de présenter des histogrammes, où chaque barre représente une classe de distances et indique la proportion de tirs se traduisant en buts. Initialement, nous avions laissé à la bibliothèque pandas le soin  de délimiter les classes, mais le résultat nuisait à la lisibilité. Si nous avions utilisé des quartiles, nous aurions perdu certaines nuances intéressantes dans les données. Les déciles auraient donné des bornes moins interprétables pour les classes. Au final, nous avons opté pour des classes représentant chacune un intervalle de dix pieds de distance.

On voit dans l'ensemble que, jusqu'à une distance de 70 pieds, plus un tir est effectué proche de la cible, plus il a de chances de se traduire en but. Ce n'est pas un constat très surprenant, car on peut penser qu'il est plus facile de viser avec précision d'une distance moins grande, et que de plus moins de joueurs ont l'opportunité de s'interposer entre le tireur et le gardien pour tenter d'intercepter la rondelle.

En regardant les graphiques, on constate cependant deux phénomènes étonnants.

![Histogramme des buts en fonction de la distance (saison 2018-2019)](figures/q5-2-20182019.png)
![Histogramme des buts en fonction de la distance (saison 2019-2020)](figures/q5-2-20192020.png)
![Histogramme des buts en fonction de la distance (saison 2020-2021)](figures/q5-2-20202021.png)

D'une part, au-delà de 70 pieds, les tirs semblent reprendre en efficacité. En effet, de 2018 à 2022, les tirs d'entre 90 et 100 pieds sont en fait plus efficaces que les tirs d'entre 40 et 50 pieds. En 2020-2021, ce sont plutôt les tirs d'entre 80 et 90 pieds qui présentent cette caractéristique. Dans toutes ces années, les tirs de plus de 70 pieds de distance sont plus efficaces en moyenne que ceux de 60 à 70 pieds. La présente visualisation ne permet par contre par de tenir compte de différents facteurs qui pourraient expliquer cela. Par exemple, est-il possible que les attaquants aient une propension plus grande à tirer de loin dans un filet désert, ou encore quand, suite à une échappée, ils ne font pas face à des défenseurs qui pourraient s'interposer? Ces deux facteurs et d'autres sans doute permettraient d'expliquer au moins en partie pourquoi les tirs de loin semblent plus efficaces que ceux de distance moyenne.

D'autre part, on remarque une différence assez importante au niveau du taux de succès des tirs les plus proches entre la saison 2018-2019 et les saisons subséquentes. Sur la base des donnés à notre disposition, nous ne nous considérons pas en mesure de faire d'hypothèses sur la raison qui explique cette différence.

Types et distance de tir
------------------------

Nous avons utilisé deux types de visualisation pour cette question. Le diagramme en aires est plus facile à lire de façon générale, mais certains «insights» n'en ressortent pas aussi bien. Un diagramme tridimensionnel présentant la distance et le type de tir sur chacun des deux axes horizontaux et la proportion de succès sur l'axe vertical est plus difficile à lire, mais fait ressortir certains points intéressants.

![Graphie en aires des buts en fonction du type de tir et de la distance (saison 2016-2017)](figures/q5-3.png)
![Graphie en aires des buts en fonction du type de tir et de la distance (saison 2016-2017)](figures/q5-3-stacked.png)

Encore une fois, afin de répondre aux exigences de l'énoncé, nous avons représenté la proportion de tirs ayant donné lieu à des buts, mais ici une représentation du nombre de tirs et de buts aurait été utile. Par exemple, les deux représentations donnent à penser que le tir de type «wrap around» est extrêmement redoutable à grande distance, mais il est permis de penser qu'il s'agit probablement simplement de bruit, d'autant qu'un tir «wrap around» à longue distance ne semble pas vraiment avoir de sens.

Cela dit, on constate que le type de tir le plus efficace dépend grandement de la distance. À courte distance, les tirs les plus efficaces identifiés plus haut sont redoutables, par exemple «deflected» et «tip in». Par contre, à plus longue distance, des types de tir qui ne ressortaient pas vraiment initialement semblent les plus efficaces, en particulier le «wrist shot» et le «backhand».



