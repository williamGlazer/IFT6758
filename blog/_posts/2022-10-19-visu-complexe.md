---
layout: post
title: Visualizations Complexes
---

Select Season 
<select id='season' onchange='refreshplot()'>
	<option value=''>...</option>
	<option value='20162017'>2016-2017</option>
	<option value='20172018'>2017-2018</option>
	<option value='20182019'>2018-2019</option>
	<option value='20192020'>2019-2020</option>
	<option value='20202021'>2020-2021</option>
	<option value='20212022'>2021-2022</option>
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
            ifrm.src = '/plots/blank.html';
        }else{
        	ifrm.src = '/plots/plotly_'+season+'_'+team+'.html';
        }
	}
</script>

<!--
Exportez les 4 tracés de zone offensive au format HTML et intégrez-les dans votre article de blog. Votre parcelle doit permettre aux utilisateurs de sélectionner n’importe quelle équipe au cours de la saison sélectionnée. Note: Parce que vous pouvez trouver ces chiffres sur internet, répondre à ces questions sans produire ces chiffres ne vous rapportera pas de points !
-->

## Unbloqued Shot Rate

Current graph represents the comparison of current team on the seasons selencted against the media of all teams on same season. 
Regions in blue are indicating that the number of shots were below the average, and in red the inverse, when the shots are over the average
A graph mainly *red* means a better performance in terms of how effective the team was shuting, and *blue* maps represents a low performance over the season.

<!--
Discutez (en quelques phrases) de ce que vous pouvez interpréter à partir de ces graphiques.
-->
Readind more in detail the plots, we can recognize the spots where most often shots were made, showing the players with best performance on each team, or in case inverse, were teams has leaks and were they need work to improve. 



---


<!--
Considérez l’Avalanche du Colorado; jetez un œil à leur carte de tir au cours de la saison 2016-17. Discutez de ce que vous pourriez dire sur l’équipe au cours de cette saison. Regardez maintenant la carte des plans de l’Avalanche du Colorado pour la saison 2020-21 et discutez de ce que vous pourriez conclure de ces différences. Est-ce que ça a du sens? Astuce : regardez le classement.
-->
### case Avalanche Colorado : a winner strategy

| Season 2016-2017 | season 2020-2021 |
| ----------- | ----------- |
| ![2016-2017](/plots/COL_2016.png) | ![2020-2021](/plots/COL_2020.png) |

This team had an amazing recovery from the last places to the top, if we see the map from 2016 - 2017, shots were performed mainly from far, lot of shots with no positive results. Their strategy changes from 2020 - 2021 when the team focus on shots very close to the net, this can be interpretated as more offensive game that become in a very effective plan.


---

### Case Buffalo Sabres vs. Tampa Lighting 

| Buffalo Sabres | Tampa Lighting |
| ----------- | ----------- |
| ![2018](/plots/BUF_2018.png) | ![2018](/plots/TBL_2018.png) |
| Season 2018-2019 | 
| ![2019](/plots/BUF_2019.png) | ![2019](/plots/TBL_2019.png) |
| Season 2019-2020 |
| ![2020](/plots/BUF_2020.png) | ![2020](/plots/TBL_2020.png) |
| Season 2020-2021 |

Here we have side to side the density maps of both teams executed on the consecutive seasons 2018-2019, 2019-2020 and 2020-2021
Tampa Lightings a remarcable team that execute lot of shots close and front the goalie, Buffalo instead shows a degradation of this main position over the years reflecting a continous underperformance regarless the shot average were increased, this is not a coincidence, in hockey primes the quality over the quantity.


<!--

Considérez les Sabres de Buffalo, une équipe qui a connu des difficultés ces dernières années, et comparez-les au Lightning de Tampa Bay, une équipe qui a remporté le Stanley deux années consécutives. Regardez les plans de tir de ces deux équipes des saisons 2018-19, 2019-20 et 2020-21. Discutez des observations que vous pouvez faire. Y a-t-il quelque chose qui pourrait expliquer le succès du Lightning, ou les luttes des Sabres ? À quel point une image est-elle complète selon vous ?
-->