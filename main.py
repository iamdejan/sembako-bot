from command.command import Command
from command.donate import DonateCommand
from command.help import HelpCommand
from command.subscribe import SubscribeCommand
from command.unsubscribe import UnsubscribeCommand
from command.unknown import UnknownCommand
from command.personal_update import PersonalUpdateCommand
from database import User
from fastapi import FastAPI
from typing import Dict
from price import get_price_updates_for_users

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
            chat_id,
            name=f'{first_name} {last_name}'
        ),
        "/unsubscribe": UnsubscribeCommand(chat_id),
        "/update": PersonalUpdateCommand(chat_id),
        "/start": HelpCommand(chat_id),
        "/help": HelpCommand(chat_id),
        "/donate": DonateCommand(chat_id)
    }
    command_str: str = payload["message"]["text"]
    if command_str not in command_map:
        UnknownCommand(chat_id).execute()
        return

    command: Command = command_map[command_str]
    command.execute()


@app.post("/prices")
def get_price_update():
    chat_ids = [int(u.id) for u in User.select(User.id)]
    get_price_updates_for_users(chat_ids)
