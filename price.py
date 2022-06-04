from bot import BotProvider
from datetime import datetime
from provider import Provider, \
    SegariProvider, \
    TokopediaProvider, \
    ShopeeMallProvider
from telegram import Bot
from typing import Optional

import pytz


def get_price_updates_for_users(chat_ids: list[int]):
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
            shop_domain="samudrasembako",
            product_key="minyak-sunco-pouch-2-liter"
        ),
        ShopeeMallProvider(
            item_id="11256156456",
            shop_id="379357698"
        )
    ]
    tz = pytz.timezone("Asia/Jakarta")
    message: str = f"*TANGGAL: {datetime.now(tz).strftime('%Y-%m-%d')}*\n\n"
    message.__add__("\n")
    for provider in providers:
        item_message: str = provider.provide_message()
        message = message + item_message + "\n"

    bot: Optional[Bot] = BotProvider.get()
    if bot is None:
        return
    for chat_id in chat_ids:
        bot.send_message(
            chat_id=chat_id,
            text=message.strip(),
            parse_mode="Markdown"
        )
