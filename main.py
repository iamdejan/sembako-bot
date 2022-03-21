from command import Command, \
    HelpCommand, \
    PersonalUpdateCommand, \
    SubscribeCommand, \
    UnknownCommand, \
    UnsubscribeCommand
from database import User
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import Bot
from typing import Dict
from price import get_price_updates_for_users

import os

load_dotenv()

bot: Bot = Bot(token=os.getenv("API_KEY").__str__())
app: FastAPI = FastAPI()


@app.get("/healthcheck")
def root_get() -> str:
    return "Hello world!"


@app.post("/")
def receive_webhook(payload: dict):
    chat_id: int = int(payload["message"]["chat"]["id"])
    first_name: str = payload["message"]["chat"]["first_name"]
    last_name: str = payload["message"]["chat"]["last_name"]
    command_map: Dict[str, Command] = {
        "/subscribe": SubscribeCommand(
            bot,
            chat_id,
            name=f'{first_name} {last_name}'
        ),
        "/unsubscribe": UnsubscribeCommand(
            bot,
            chat_id
        ),
        "/update": PersonalUpdateCommand(
            bot,
            chat_id
        ),
        "/start": HelpCommand(
            bot,
            chat_id
        ),
        "/help": HelpCommand(
            bot,
            chat_id
        )
    }
    command: str = payload["message"]["text"]
    if command not in command_map:
        UnknownCommand(bot, chat_id).execute()
        return

    command_map[command].execute()


@app.post("/prices")
def get_price_update():
    chat_ids = [int(u.id) for u in User.select(User.id)]
    get_price_updates_for_users(bot, chat_ids)
