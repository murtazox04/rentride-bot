FROM python:3.10-alpine

RUN pip install --upgrade pip

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "main:app", "--port=8080", "--reload" ]