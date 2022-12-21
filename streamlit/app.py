import pandas as pd
import streamlit as st
from ift6758.network import GameClient, ServingClient

st.title('Hockey Match Prediction')

# SIDEBAR
with st.sidebar:
    workspace = st.text_input('Workspace', value='williamglazer')
    model = st.text_input('Model', value='naive-bayes')
    version = st.text_input('Version', value='1.0.0')

    if st.button('load model'):
        # trigger post request to container
        # animation upon loading
        # validate if model exists
        # if not warn
        # if success display load successfull
        pass


# BODY
id = st.text_input('game id', value=2021020001)

if st.button('evaluate game'):
    # validate if game id is legal
    # TODO

    # fetching data
    with st.spinner('Fetching data from NHL API'):
        data = GameClient.get_game_data(id)

    # post request to container
    with st.spinner('Predicting data from models'):
        result = ServingClient().predict(data)

    df = pd.concat([data, result], axis=1)
    col_1, col_2 = st.columns(2)

    # display expected goals
    team_1, team_2 = df.offense_team_name.unique()
    for team, col in [(team_1, col_1), (team_2, col_2)]:
        with col:
            team_plays = df[df.offense_team_name == team]
            team_xg = team_plays.goal_proba.sum()
            team_goals = team_plays.goal.sum()
            st.metric(
                f'{team} (Expected Goals / Truth)',
                f'{round(team_xg, 2)} / {team_goals}',
                delta=round(team_xg-team_goals, 2)
            )

    # if yes display results and dataframe
    st.dataframe(df)
