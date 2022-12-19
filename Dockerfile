FROM python:3.9

# working directory whithin the docker container (linux) 
WORKDIR /
#WORKDIR /notebooks

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt --use-feature=2020-resolver


#copy local into container - keep same folder name
COPY ./ift6758 ./ift6758

COPY ./notebooks ./notebooks

COPY ./figures ./figures

COPY ./blog ./blog

EXPOSE 8888

#environment variable
ENV DISPLAY=:0

#Volumes
ADD . /logs

#env variable for comet
#ENV COMET_API=

#ENTRYPOINT ["jupyter","lab","--ip=0.0.0.0","--allow-root"]
ENTRYPOINT ["jupyter","notebook","--ip=0.0.0.0","--allow-root"]


