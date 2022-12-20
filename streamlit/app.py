import streamlit as st

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
id = st.text_input('game id')

if st.button('evaluate game'):
    # trigger post request to container
    # animation upon loading
    # validate if game id is legal
    # if not warn
    # if yes display results and dataframe
    pass
