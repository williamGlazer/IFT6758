# IFT6758

## How to run the app

first set the comet api environment variable with 
```bash
export COM_API_KEY=${comet_key}
```

then run the docker compose which will build and serve the images
```bash
bash run-app.sh
```

finally open the urls to view the app
1. [for streamlit](localhost:8501)
1. [for server logs](localhost:8080/logs)


## Repo Contents

- `/blog`: contents of jekyll blog theme for handins
- `/figures`: plots generated from our codebase
- `/ift6758`: contains code used throughout the project
  - `ift6758/data`: NHL API data extraction
  - `ift6758/network`: endpoints to interact with the server
  - `ift6758/pipeline`: experiment pipeline to train our models
  - `ift6758/vizualisations`: code to generate `/figures`
- `/notebooks`: notebooks to illustrate how to use our repository
- `/server`: standalone flask server to serve our model
- `/streamlit`: website to interact with our models

## Commands:

- `run-app.sh`: runs the entire application by calling docker-compose-up
- `run-server.sh`: runs the server as a standalone backend
- `run-streamlit.sh`: runs the website which depends on the backend server
- `run-build-docker.sh`: triggers the build for the two docker images
