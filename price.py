from bot import BotProvider
from datetime import datetime
from provider import Provider, \
    SegariProvider
from telegram import Bot
from typing import Optional

import pytz


def get_price_updates_for_users(chat_ids: list[int]):
    bot: Optional[Bot] = BotProvider.get()
    if bot is None:
        return

    providers: list[Provider] = [
        SegariProvider(
            "Susu Greenfields Cokelat 1 Liter"
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
        SegariProvider(
            "Kecap Manis Bango Pouch"
        ),
        SegariProvider(
            "Kecap Asin Lee Kum Kee"
        ),
        SegariProvider(
            "Minyak Zaitun Filippo Berio"
        ),
        SegariProvider(
            "Minyak Goreng Filma 2 L"
        ),
        SegariProvider(
            "Ayyomi Telur Ayam Kampoeng"
        )
    ]
    tz = pytz.timezone("Asia/Jakarta")
    message: str = f"*TANGGAL: {datetime.now(tz).strftime('%Y-%m-%d')}*\n\n"
    message.__add__("\n")
    for provider in providers:
        item_message: str = provider.provide_message()
        message = message + item_message + "\n"
        print(f"completed item_message = {item_message}")

    for chat_id in chat_ids:
        bot.send_message(
            chat_id=chat_id,
            text=message.strip(),
            parse_mode="Markdown"
        )
