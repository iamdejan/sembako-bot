from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import Bot
from provider import Provider, \
    SegariProvider, \
    TokopediaProvider, \
    ShopeeMallProvider
from playhouse.cockroachdb import CockroachDatabase
from peewee import Model, BigIntegerField, CharField
from utils import give_help, inform_unknown_command

import os

load_dotenv()

# TODO: temporary logic, future logic will use GCP secrets
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


bot: Bot = Bot(token=os.getenv("API_KEY").__str__())
app: FastAPI = FastAPI()


@app.get("/healthcheck")
def root_get() -> str:
    return "Hello world!"


@app.post("/execute")
def execute():
    chat_ids = [int(u.id) for u in User.select(User.id)]

    providers: list[Provider] = [
        SegariProvider(
            "Sari Roti - Roti Tawar Special"
        ),
        SegariProvider(
            "Tous Les Jours - Burger Bun Wijen"
        ),
        SegariProvider(
            "Susu Greenfields Cokelat 1 Liter"
        ),
        SegariProvider(
            "Gula Rose Brand Premium 1 Kg"
        ),
        SegariProvider(
            "Sosis Sapi Bratwurst Kanzler"
        ),
        SegariProvider(
            "Indomie Goreng Bundle Isi 5"
        ),
        SegariProvider(
            "Nugget Ayam Fiesta"
        ),
        SegariProvider(
            "Spicy Wing Fiesta"
        ),
        SegariProvider(
            "Beras Setra Ramos Topi Koki"
        ),
        TokopediaProvider(
            shop_domain="unilever-food",
            product_key="twin-pack-bango-kecap-manis-6-2kg"
        ),
        TokopediaProvider(
            shop_domain="abc-official",
            product_key="abc-kecap-asin-6-kg"
        ),
        TokopediaProvider(
            shop_domain="finger-land",
            product_key="borges-extra-light-olive-oil-minyak-zaitun-5-l"
        ),
        TokopediaProvider(
            shop_domain="needlife",
            product_key="sunco-minyak-goreng-refill-2l"
        ),
        ShopeeMallProvider(
            item_id=11256156456,
            shop_id=379357698
        )
    ]
    for provider in providers:
        message = provider.provide_message()
        for chat_id in chat_ids:
            bot.send_message(
                chat_id=chat_id,
                text=message
            )


@app.post("/")
def receive_webhook(payload: dict):
    command = payload["message"]["text"]
    # TODO: refactor, use strategy pattern
    if command == "/register":
        register(payload)
    elif command == "/unregister":
        unregister(payload)
    elif command == "/start" or command == "/help":
        give_help(bot=bot, chat_id=int(payload["message"]["chat"]["id"]))
    else:
        inform_unknown_command(bot=bot, chat_id=int(payload["message"]["chat"]["id"]))


def register(payload: dict):
    chat_id = int(payload["message"]["chat"]["id"])
    name = f'{payload["message"]["chat"]["first_name"]} {payload["message"]["chat"]["last_name"]}'
    with db.transaction():
        User.insert(id=chat_id, name=name).on_conflict_replace().execute()
        bot.send_message(
            chat_id=chat_id,
            text="Selamat! Anda sudah terdaftar."
        )


def unregister(payload: dict):
    chat_id = int(payload["message"]["chat"]["id"])
    with db.transaction():
        User.delete().where(User.id == chat_id).execute()
        bot.send_message(
            chat_id=chat_id,
            text="Anda tidak terdaftar lagi."
        )
