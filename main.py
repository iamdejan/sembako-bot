from dotenv import load_dotenv
from fastapi import FastAPI
from markdown_builder.document import MarkdownDocument
from telegram import Bot
from provider import Provider, SegariProvider, TokopediaProvider

import os

load_dotenv()

bot: Bot = Bot(token=os.getenv("API_KEY").__str__())
app: FastAPI = FastAPI()


@app.get("/")
def root_get() -> str:
    return "Hello world!"


@app.post("/execute")
def execute():
    providers: list[Provider] = [
        TokopediaProvider(
            shop_domain="rafaeyzaparfume",
            product_key="minyak-goreng-minyak-sayur-sunco-2l"
        ),
        SegariProvider(
            "Beras Setra Ramos Topi Koki"
        ),
        SegariProvider(
            "Gula Rose Brand Premium 1 Kg"
        ),
        SegariProvider(
            "Sosis Sapi Bratwurst Kanzler"
        ),
        SegariProvider(
            "Nugget Ayam Fiesta"
        ),
        SegariProvider(
            "Spicy Wing Fiesta"
        ),
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
            "Indomie Goreng Bundle Isi 5"
        )
    ]
    for provider in providers:
        bot.send_message(
            chat_id="1661005444",
            text=provider.provide_message()
        )
