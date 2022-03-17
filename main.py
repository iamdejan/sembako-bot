from dotenv import load_dotenv
from fastapi import FastAPI
from markdown_builder.document import MarkdownDocument
from telegram import Bot
from provider import Provider, TokopediaProvider

import os

load_dotenv()

bot: Bot = Bot(token=os.getenv("API_KEY").__str__())
app: FastAPI = FastAPI()


@app.get("/")
def root_get() -> str:
    return "Hello world!"


@app.post("/execute")
def execute():
    shop_domain = "rafaeyzaparfume"
    product_key = "minyak-goreng-minyak-sayur-sunco-2l"
    cooking_oil_provider: Provider = TokopediaProvider(
        shop_domain,
        product_key
    )
    bot.send_message(
        chat_id="1661005444",
        text=cooking_oil_provider.provide_message()
    )
