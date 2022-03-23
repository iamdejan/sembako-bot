from dotenv import load_dotenv
from playhouse.cockroachdb import CockroachDatabase
from peewee import Model, BigIntegerField, CharField

import os

load_dotenv()

db_user: str = os.getenv("DB_USER").__str__()
db_password: str = os.getenv("DB_PASSWORD").__str__()
db_host: str = os.getenv("DB_HOST").__str__()
db_port: str = os.getenv("DB_PORT").__str__()
db_cluster: str = os.getenv("DB_CLUSTER").__str__()
db_name: str = os.getenv("DB_NAME").__str__()
db_string: str = os.getenv("DB_STRING").__str__() or \
    f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=verify-full&options=--cluster%3D{db_cluster}'
db: CockroachDatabase = CockroachDatabase(db_string)


class User(Model):
    id = BigIntegerField(primary_key=True)
    name = CharField(max_length=255)

    class Meta:
        database = db
        table_name = 'users'
