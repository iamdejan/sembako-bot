FROM python:3.9.10-slim-bullseye

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

RUN apt update && \
    apt install curl && \
    curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/392cd414-c163-46d8-bc80-b8c0dccbfb34/cert

EXPOSE 8000
ENV API_KEY ${API_KEY}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
