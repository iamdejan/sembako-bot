FROM python:3.9.10-slim-bullseye

WORKDIR /app
COPY . .

RUN apt update -y && \
    apt install -y curl python3-psycopg2 libpq-dev gcc && \
    curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/392cd414-c163-46d8-bc80-b8c0dccbfb34/cert

RUN pip3 install -r requirements.txt

EXPOSE 8000
ENV API_KEY ${API_KEY}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
