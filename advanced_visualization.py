
from typing import Tuple
from ipywidgets      import widgets,interact,interactive
from IPython.display import display
import pandas as pd
import os
from pathlib import Path
import plotly.graph_objects as go
from PIL import Image
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


'''
csv data format

    "game starttime",
    "game endtime",
    "gameId",                counter
    "offense_team_id",       when event=goal|shot     team offenser 
    "offense_team_name",     when event=goal|shot     team name
    "offense_team_tricode",  when event=goal|shot     team tricode
    "goal",                  goal = 1 | shot= 0
    "x_coords",              
    "y_coords",
    "goalie_id",             goalkeeper 
    "goalie_name",           goalkeeper
    "shooter_id",
    "shooter_name",
    "shot type",
    "empty net",
    "strength_shorthand",
    "strength_even",
    "strength_powerplay",
'''
full_path = os.getcwd()
root_path = str(Path(full_path).parents[0])

#define initial parameters
im2     = Image.open(r'{r}/IFT6758/figures/nhl_rink_top.png'.format(r=root_path)) 
seasons = ['20162017','20172018','20182019','20192020', '20202021']
teams   = ['NOP','NJD','NYI','NYR','PHI','PIT','BOS','BUF','MTL','OTT','TOR','FLA','WSH','CHI','DET','NSH','STL','CGY','COL','EDM','VAN','ANA','DAL','LAK','SJS','CBJ','MIN','WPG','ARI','VGK','SEA']


# transpose cordinate Y
# We will assume that all shots were realized from the opponent side. 
# but a more precise results will require to know the rink side at time
# of the shot for current team

def transposeX(xval, yval):
    xval = float(xval)
    yval = float(yval)
    if xval < 0 :
        xval = xval*(-1)
    xval -= 89.0
    return xval*(-1)

def transposeY(xval, yval):
    xval = float(xval)
    yval = float(yval)
    if xval < 0 :
        yval = yval*(-1)
    return yval

# create dash App
app = dash.Dash()

@app.callback(
    Output(component_id='season-graph', component_property='figure'),
    [Input(component_id='season', component_property='value'),
    Input(component_id='team', component_property='value')]
)



 #based on season and team, draw all shooting point on the map
 

def update_graph(season,team):
    
    # Create figure
    fig = go.Figure()
    
    print('season: {s} team: {t} '.format(s=season,t=team))
    
    # load data for selected season / team
    csv_path  = root_path+'/IFT6758/ift6758/data/tabular/'+season+'.csv'
    df = pd.read_csv(csv_path)
    
    # league shoot count , create unique key
    df['team_game'] = df.apply(lambda row: str(row['game starttime'])+str(row['offense_team_tricode']), axis=1)
    l_shoot_count  =  df.shape[0] 
    
    # all teams season games counter
    season_games_counter = df['team_game'].unique().shape[0]
    
    # Filter data leaving only current team
    df_team = df[df['offense_team_tricode'] == team].copy()
    
    # total shots on current game is equal at number of records on this date for this team 
    team_season_games = df_team['game starttime'].unique().shape[0]    
    
    '''  start funny thing ''' 
    # ----------------------------------------------------------------------------
    # build [excess_shot_rate] row, that represent on a tile size="tile_sz" 
    # the difference between the average shot on this tile for all teams all games
    # and the current number of shoots for the current team
    # ----------------------------------------------------------------------------
    
    tile_sz = 5 
    x_range = list(range(-100,100,tile_sz))
    y_range = list(range( -50, 50,tile_sz))
    
    for xval in x_range:
        for yval in y_range:
            # all shoot inside the current tile
            tile_shots = df.loc[(df['x_coords'] >= xval         ) & 
                                (df['x_coords'] < (xval+tile_sz)) & 
                                (df['y_coords'] >= yval         ) &
                                (df['y_coords'] < (yval+tile_sz)) ]
            tile_count = tile_shots.shape[0]
            tile_mean_per_game  = tile_count/season_games_counter
            # team shoot inside current tile
            teamtile_shoots = df_team.loc[(df_team['x_coords'] >= xval         ) & 
                                          (df_team['x_coords'] < (xval+tile_sz)) & 
                                          (df_team['y_coords'] >= yval         ) &
                                          (df_team['y_coords'] < (yval+tile_sz)) ]
            tg_shoots = teamtile_shoots.shape[0]
            tile_mean_per_game_per_team = tg_shoots/team_season_games
            #find all records that match this coordinates to include the value 
            for idx in teamtile_shoots.index:
                df_team.loc[idx,'excess_shot_rate'] = tile_mean_per_game_per_team -  tile_mean_per_game 
                
    '''  ends funny thing ''' 
    # Transpose X and Y based on current localization  
    df_team['y_abs'] = df_team.apply(lambda row: transposeX(row.x_coords,row.y_coords),axis = 1)
    df_team['x_abs'] = df_team.apply(lambda row: transposeY(row.x_coords,row.y_coords),axis = 1)


    colorscale = [[0, 'Blue'], [0.5, 'white'], [1, 'Red']]
    # Trace test 03 : Contour
    
    fig.add_trace(
        go.Contour(
            z=df_team.loc[:, 'excess_shot_rate'],
            x=df_team.loc[:, 'x_abs'],
            y=df_team.loc[:, 'y_abs'],
            opacity=0.6,
            colorscale=colorscale
        #colorscale='Viridis'
        )
    )
    
   
    # Add background image with the game limits
    fig.add_layout_image(
        dict(
            source=im2,
            xref="x",
            yref="y",
            x=-42.5,   # dims in feet
            y=-11,
            sizex=85,
            sizey=100,
            sizing="stretch",
            layer="below"
        )
    )
    
    # reverse Y axis to be top-down direction
    fig.update_yaxes(
        autorange="reversed"
    )
    
    # header title -------------------------- 
    fig.add_annotation(x=.5, y=-32,
            text="Unblocked Shot Rate",
            showarrow=False,
            font=dict(
                family="verdana, Arial",
                size=18, 
                color="#333333",
            )
    )
    # header Description -------------------- 
    fig.add_annotation(x=.5, y=-22,
            text='season: {s} team: {t} '.format(s=season,t=team),
            showarrow=False,
            font=dict(
                family="verdana, Arial",
                size=16, 
                color="#888888",
            )
    )
    
    # axes, scales and margins --------------
    fig.update_layout(
        showlegend=False,
        xaxis_title="Distace from centre of rink (ft)",
        yaxis_title="Distance from goal line (ft)",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#333333"
        ),
        width=85*8,
        height=100*8,
        autosize=True,
        margin=dict(t=50, b=0, l=50, r=0), # graph margins
        template="plotly_white"
    )
    #save locally a static html page
    fig.write_html('blog/_posts/plotly_{s}_{t}.html'.format(s=season,t=team), include_plotlyjs=True)
    return fig 

    

#create app layout
app.layout = html.Div(children=[
    html.H1(children='Unbloqued Shot Rate'),
    dcc.Dropdown(id='season',options=seasons, value='20162017'),
    dcc.Dropdown(id='team'  ,options=teams,   value='MTL'),
    dcc.Graph(id='season-graph')
])




if __name__ == '__main__':
    app.run_server(debug=True)
    


