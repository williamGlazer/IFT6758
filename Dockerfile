FROM python:3.9


RUN mkdir "project"
WORKDIR project

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt


COPY ./server/app.py .
COPY ./ift6758 ./ift6758
RUN mkdir -p "data/models/staging"

EXPOSE 8080

CMD ["gunicorn","--bind=0.0.0.0:8080","app:app"]