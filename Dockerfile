FROM python:3.11
LABEL authors="holly"

WORKDIR /app

COPY requirements.txt /app
COPY .env /app
COPY src /app/src

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "/app/src/slash-commands.py"]