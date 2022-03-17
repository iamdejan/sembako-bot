from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import Bot
from provider import Provider, SegariProvider, TokopediaProvider, ShopeeMallProvider

import os

load_dotenv()

chat_ids: list[str] = os.getenv("CHAT_IDS").__str__().strip().split(",")
bot: Bot = Bot(token=os.getenv("API_KEY").__str__())
app: FastAPI = FastAPI()


@app.get("/")
def root_get() -> str:
    return "Hello world!"


@app.post("/execute")
def execute():
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
