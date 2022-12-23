#!/bin/bash

docker build --tag nhlserver --file Dockerfile.serving .
docker build --tag nhlweb --file Dockerfile.streamlit .