FROM python:3.9.10-slim-bullseye

WORKDIR /app
COPY . .

# need to install libpq-dev and gcc, see https://stackoverflow.com/a/67404591
RUN apt update -y && \
    apt install -y curl libpq-dev gcc && \
    curl --create-dirs -o /root/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/392cd414-c163-46d8-bc80-b8c0dccbfb34/cert

RUN pip3 install -r requirements.txt

EXPOSE 8000
ENV API_KEY ${API_KEY}
ENV DB_STRING ${DB_STRING}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
