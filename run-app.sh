#!/bin/bash

if [ -z ${COMET_API_KEY} ];
then
    echo "please set env var COMET_API_KEY"
else
    docker-compose up
fi