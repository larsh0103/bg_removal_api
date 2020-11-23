FROM python:3.8

WORKDIR /.
COPY ./ .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements-api.txt

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]