FROM python:3.8

WORKDIR /.
COPY /requirements-api.txt .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements-api.txt

COPY ./ .
ENV PORT 8080

EXPOSE 8080

RUN python download_models.py

CMD python app.py