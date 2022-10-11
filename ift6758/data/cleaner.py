
import pandas as pd
import json


class NHLConverter:
    """
    Class to convert data from raw json to interpretable table with following constraints
    "all events of every game into a pandas dataframe,include events of the type “shots” and “goals”, ignore missed shots or blocked shots for now"
    Features :  
        - game time/period information, 
        - game ID, team information (which team took the shot), 
        - indicator if its a shot or a goal, 
        - the on-ice coordinates, 
        - the shooter  
        - goalie name (don’t worry about assists for now), 
        - shot type, 
        - if it was on an empty net
        - whether or not a goal was at even strength, shorthanded, or on the power play
    """
    # liveData/plays/
    def __init__(self, json_fn: str) -> None:
        self.json_fn = json_fn
        
    def pull_json(self) -> None:  
        f = open(self.json_fn)
        loaded_data = json.load(f)

        if len(loaded_data.keys()) == 1:        # Store dictionary with shot info, remove copyright
            # print(loaded_data[list(loaded_data.keys())[0]])
            
            self.raw_data = loaded_data[list(loaded_data.keys())[0]]
            print(len(self.raw_data))
        else:
            print('Wrong format')


    def convert_season(self) -> pd.DataFrame:

        cols = ['game starttime', 'game endtime', 'gameId','offense_team_id', 'offense_team_name', 'offense_team_tricode','goal', 'x_coords', 'y_coords', 'goalie_id', 'goalie_name', 'shooter_id', 'shooter_name', 'shot type', 'empty net', 'strength_shorthand', 'strength_even', 'strength_powerplay']
        selec_data = []
        game_id = 0
        for game in self.raw_data:
            # print(game_id)
            game_endtime = game['gameData']['datetime']['endDateTime']
            game_starttime = game['gameData']['datetime']['dateTime']
            
            event_list = game['liveData']['plays']['allPlays']
            
            for event in event_list: 
                if event['result']['event'] == 'Shot' or event['result']['event'] == 'Goal':

                    curr_event = [game_starttime, game_endtime, game_id]
                    curr_event.append(event['team']['id'])
                    curr_event.append(event['team']['name'])
                    curr_event.append(event['team']['triCode'])
                    # curr_event.append(event['result']['event'])
                    curr_event.append(0 if event['result']['event']== 'Shot' else 1)
                    curr_event.append(event['coordinates'].get('x', None))
                    curr_event.append(event['coordinates'].get('y', None))
                    for p in event['players']:
                        if p['playerType'] == 'Goalie':
                            goalie_id = p['player']['id']
                            goalie_name = p['player']['fullName']
                        elif p['playerType'] == 'Shooter' or p['playerType'] == 'Scorer':
                            shooter_id = p['player']['id']
                            shooter_name = p['player']['fullName']
                    curr_event.append(goalie_id)
                    curr_event.append(goalie_name)
                    curr_event.append(shooter_id)
                    curr_event.append(shooter_name)
                    
                    curr_event.append(event['result'].get('secondaryType', None))

                    if event['result']['event'] == 'Goal':
                        curr_event.append(event['result'].get('emptyNet', None))
                        ## 
                        if event['result']['strength'].get('code', None) == 'EVEN': 
                            curr_event.append(0)
                            curr_event.append(1)
                            curr_event.append(0)
                        elif event['result']['strength'].get('code', None) == 'PPG': 
                            curr_event.append(0)
                            curr_event.append(0)
                            curr_event.append(1)
                        else: 
                            curr_event.append(1)
                            curr_event.append(0)
                            curr_event.append(0)
                    else:
                        curr_event.append(False)
                        curr_event.append(None)

                    
                    selec_data.append(curr_event)
                    game_id+=1
        print(game_id)

        return pd.DataFrame(selec_data, columns=cols)

        
    