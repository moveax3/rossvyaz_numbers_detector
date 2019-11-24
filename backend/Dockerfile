FROM python:3.8-alpine
RUN apk update
RUN apk add --no-cache musl-dev postgresql-dev gcc python3-dev
WORKDIR /usr/src/app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
