# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]