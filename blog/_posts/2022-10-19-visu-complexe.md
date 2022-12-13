---
layout: post
title: Visualizations Complexes
---

<!--
Exportez les 4 tracés de zone offensive au format HTML et intégrez-les dans votre article de blog. Votre parcelle doit permettre aux utilisateurs de sélectionner n’importe quelle équipe au cours de la saison sélectionnée. Note: Parce que vous pouvez trouver ces chiffres sur internet, répondre à ces questions sans produire ces chiffres ne vous rapportera pas de points !
-->

## Densité de tirs

Le graphique montre la densité de tirs sur la glace pour une équipe/saison donnée. La moyenne (blanche) est la moyenne de tirs de toutes les équipes pour une saison donnée. On peut voir les régions chaudes (en rouge) qui représentent des régions ou plus de but ont été marqués que la moyenne des équipe. En bleu on a l'opposé, soit en-dessous de la moyenne.

Dans ces graphes, on peut voir de quel régions les différentes équipes arrivent à marquer leurs buts. Est-ce qu'il s'agit d'une équipe qui amrque beaucoup de buts à proximitée de manière aggresive, qui domine le centre de la glace, ou est-ce plutôt une équipe qui préfère tirer souvent, mais de loin avec des coups du poignet.

Ceci nous permet de voir l'efficacité des startégies et les différentes faiblesses des équipes.


Select Season  
Fixed to 2016-2018 for hand-in due to filesize exceeding gradescope limits otherwise

<select id='season' onchange='refreshplot()'>
	<option value='20162017'>2016-2017</option>
	<option value='20172018'>2017-2018</option>
</select>

Select Team 
<select id='team' onchange='refreshplot()'>
	<option value=''>..</option>
	<option value='ANA'>Mighty Ducks of Anaheim/Anaheim Ducks</option>
	<option value='ARI'>Arizona Coyotes</option>
	<option value='BOS'>Boston Bruins</option>
	<option value='BUF'>Buffalo Sabres</option>
	<option value='CAR'>Carolina Hurricanes</option>
	<option value='CBJ'>Columbus Blue Jackets</option>
	<option value='CGY'>Calgary Flames</option>
	<option value='CHI'>Chicago Black Hawks/Blackhawks</option>
	<option value='COL'>Colorado Avalanche</option>
	<option value='DAL'>Dallas Stars</option>
	<option value='DET'>Detroit Red Wings</option>
	<option value='EDM'>Edmonton Oilers</option>
	<option value='FLA'>Florida Panthers</option>
	<option value='LAK'>Los Angeles Kings</option>
	<option value='MIN'>Minnesota Wild</option>
	<option value='MTL'>Montreal Canadiens</option>
	<option value='NJD'>New Jersey Devils</option>
	<option value='NSH'>Nashville Predators</option>
	<option value='NYI'>New York Islanders</option>
	<option value='NYR'>New York Rangers</option>
	<option value='OTT'>Ottawa Senators</option>
	<option value='PHI'>Philadelphia Flyers</option>
	<option value='PIT'>Pittsburgh Penguins</option>
	<option value='SJS'>San Jose Sharks</option>
	<option value='STL'>St. Louis Blues</option>
	<option value='TBL'>Tampa Bay Lightning</option>
	<option value='TOR'>Toronto Maple Leafs</option>
	<option value='VAN'>Vancouver Canucks</option>
	<option value='WPG'>Winnipeg Jets</option>
	<option value='WSH'>Washington Capitals</option>
</select>
 <iframe id="iframe" src="/plots/blank.html" style="height:830px;width:100%; border:dotted 1px #999;" title="plot"></iframe> 
<script>
	function refreshplot(){
		let season = document.getElementById('season').value;
		let team   = document.getElementById('team').value;
		let ifrm   = document.getElementById('iframe');
        if((season=='')||(team=='')){
            ifrm.src = 'plots/blank.html';
        }else{
        	ifrm.src = 'plots/plotly_'+season+'_'+team+'.html';
        }
	}
</script>

---


<!--
Considérez l’Avalanche du Colorado; jetez un œil à leur carte de tir au cours de la saison 2016-17. Discutez de ce que vous pourriez dire sur l’équipe au cours de cette saison. Regardez maintenant la carte des plans de l’Avalanche du Colorado pour la saison 2020-21 et discutez de ce que vous pourriez conclure de ces différences. Est-ce que ça a du sens? Astuce : regardez le classement.
-->
### Avalanche Colorado : une stratégie gagnante

| Season 2016-2017                 | season 2020-2021                  |
|----------------------------------|-----------------------------------|
| ![2016-2017](plots/COL_2016.png) | ![2020-2021](plots/COL_2020.png) |

Les avalanches se situaient en dernière place de leur division en 2016-2017 et on fait une remontée fulgurante en 2020-2021 pour se hisser au top de leur classement. On peut voir qu'ils avaient de la difficulté auparavant à s'approcher du gardien et que la majoritée de leurs buts étaient marqués de loin.

Leur stratégie dans la dernière saison a beaucoup évoluée et ils sont désormais capables de s'approcher du but ce qui leur donne davantage d'occasions de marquer.

---

### Buffalo Sabres vs. Tampa Lighting 

| Year      | Buffalo Sabres               | Tampa Lighting               |
|-----------|------------------------------|------------------------------|
| 2018-2019 | ![2018](plots/BUF_2018.png) | ![2018](plots/TBL_2018.png) |
| 2019-2020 | ![2019](plots/BUF_2019.png) | ![2019](plots/TBL_2019.png) |
| 2020-2021 | ![2020](plots/BUF_2020.png) | ![2020](plots/TBL_2020.png) |

La comparaison côte-à-côte montre que le Lightning, qui connait beaucoup de succès, priorise des tris proche du centre de la glace et proche du gardien. Ils réussissent donc à déjouer la défence et s'approcher du but, ce qui leur donne un beaucoup plus haut taux de succès. 

Buffalo quand a eux on des tirs beaucoup plus disparates avec un faible taux de succès. Leurs régions à haute densitée de succès sont beaucoup plus disparates.

Il semble facile d'expliquer la différence de perforamnce selon ces graphiques!