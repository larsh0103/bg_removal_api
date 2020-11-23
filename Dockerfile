FROM python:3.8

WORKDIR /.
COPY ./ .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements-api.txt

ENV PORT 8080

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app