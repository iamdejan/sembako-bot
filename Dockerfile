FROM python:3.9.10-bullseye

WORKDIR /app
COPY main.py mypy.ini requirements.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 8000
ENV API_KEY ${API_KEY}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
