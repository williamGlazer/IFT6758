import pandas as pd
import streamlit as st
from ift6758.network import GameClient, ServingClient
from datetime import datetime, timezone, timedelta

def ping_game(id):
    # fetch index of last predicted event
    if id in predicted_cache:
        prev_predicted = predicted_cache[id]
        last_event_idx = prev_predicted.shape[0]
    else:
        last_event_idx = 0

    # fetching data
    with st.spinner('Fetching data from NHL API'):
        data = GameClient.get_game_data(id)
    to_predict = data.iloc[last_event_idx:,:]

    # post request to container
    with st.spinner('Predicting data from models'):
        result = serving_client.predict(to_predict)

    df = pd.concat([to_predict, result], axis=1)
    if id in predicted_cache:
        df = pd.concat([prev_predicted, df], axis=0)

    team_1, team_2 = df.offense_team_name.unique()

    st.header(f'Game {id}: {team_1} vs. {team_2}')
    end_time = datetime.strptime(df.iloc[1].loc["game_starttime"], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)
    end_time = end_time.replace(tzinfo=timezone.utc)

    if end_time > datetime.now(tz=timezone.utc):
        time_left = end_time - datetime.now(tz=timezone.utc)
        period = 3 - ((time_left.seconds/60) // 20)
    else:
        time_left = 0
        period = 'Over'
    

    st.text(f'Period {period} - {time_left} minutes left')

    col_1, col_2 = st.columns(2)

    # display expected goals
    st.header('Data used for predictions (and predictions)')
    for team, col in [(team_1, col_1), (team_2, col_2)]:
        with col:
            team_plays = df[df.offense_team_name == team]
            team_xg = team_plays.goal_proba.sum()
            team_goals = team_plays.goal.sum()
            st.metric(
                f'{team} xG (actual)',
                f'{round(team_xg, 2)} ({team_goals})',
                delta=round(team_xg-team_goals, 2)
            )

    # display results and dataframe
    st.dataframe(df)

    

predicted_cache = {}

st.title('Hockey Match Prediction')

serving_client = ServingClient(ip="server")

# SIDEBAR
with st.sidebar:
    st.header('Model Selection')

    # inputs
    workspace = st.text_input('Workspace', value='williamglazer')
    model = st.text_input('Model', value='naive-bayes')
    version = st.text_input('Version', value='1.0.0')

    if st.button('load model'):
        # trigger post request to container
        with st.spinner('loading model'):
            status = serving_client.download_registry_model(workspace, model, version)

        # display request status
        if status['success']:
            st.success('model loaded')
        else:
            st.error('model loading failed')

    # display supported models
    st.text('Current Supported models:\n- naive-bayes\n- gradient-boost\n- adaboost-stratified\n- quadratic-discriminant')

# BODY
id = st.text_input('game id', value=2021020001)

if st.button('Ping Game'):
    ping_game(id)

