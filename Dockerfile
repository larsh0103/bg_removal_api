FROM python:3.8

# Copy local code to the container image.
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


COPY /requirements-api.txt .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements-api.txt


ENV PORT 8080

EXPOSE ${PORT}

RUN python download_models.py

# RUN apt-get update && apt-get install libgtk2.0-dev

CMD exec uvicorn --host 0.0.0.0 --port ${PORT} app.main:app