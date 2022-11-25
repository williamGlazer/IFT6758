## Caracteristiques Créées

[Expérience WPG V WSH](https://www.comet.com/williamglazer/hockeyanalysis/7bc807a88fb649d4a28beed00d2b5faf?experiment-tab=assets)

### Caracteristiques issue de Ingé I
- `goal`:Est un but (0 ou 1)
- `empty_net`: Filet vide (0 ou 1, vous pouvez supposons que les NaN sont 0)
- `game_secs`: Secondes de jeu (Game seconds)
- `period`: Période de jeu (Game period)
- `x_coords`, 'y_coords': Coordonnées (x,y, colonnes séparées)
- `shot_distance`: Distance de tir (Shot distance)
- `shot_angle`: Angle de tir (Shot angle)
- `shot_type`: Type de tir (Shot type)

### Fondée sur l'evenement précédent:
- `prev_type`: Dernier type d'événement (Last event type)
- `prev_x_coords`, 'prev_y_coords': Coordonnées du dernier événement (x, y, colonnes séparées)
- `prev_datetime`: Temps de l'evenement précédent
- `time_lapsed_prev_event_in_seconds`: Temps écoulé depuis le dernier événement (secondes) 
- `dist_prev_event`: Distance depuis le dernier événement (Distance from the last event)
- `rebound`: Rebond (bool) : Vrai si le dernier événement était aussi un tir, sinon False
- `angle_change`: Changement d'angle de tir: Inclure seulement si le tir est un rebond, sinon 0.
- `speed`: Vitesse


### Autres
- `season`: Saison
- `game_starttime`, 'game_endtime': Moment de début et de fin du jeu (format datetime: date, heure, minute, secondes)
- `game_id`: Code/Id du jeu
- `datetime`: Moment de l'évenement
- `offense_team_id`, 'offense_team_name', 'offense_team_tricode': Informations de l'équipe offensive (Id, Nom, Tricode, colonnes séparées)        
- `shooter_name`: Nom du tireur
- `shooter_id`: Id du tireur
- `goalie_name`: Nom du gardien
- `goalie_id`: Id du gardien
- `period_time`: Temps en secondes depuis le debut de la periode
- `strength_shorthand`, 'strength_even', 'strength_powerplay' : One-Hot-Encoding (1 si vrai 0 si faux) de la force en nombre des equipes
       
       
       