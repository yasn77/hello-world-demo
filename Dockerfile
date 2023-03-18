FROM python:3.11-slim

EXPOSE 8000

COPY src/hello_world /src/

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "gunicorn", "--bind=0.0.0.0:8000", "hello:app" ]
