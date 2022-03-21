from provider import Provider, \
    SegariProvider, \
    TokopediaProvider, \
    ShopeeMallProvider
from telegram import Bot

def get_price_updates_for_users(bot: Bot, chat_ids: list[int]):
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
            item_id="11256156456",
            shop_id="379357698"
        )
    ]
    for provider in providers:
        message = provider.provide_message()
        for chat_id in chat_ids:
            bot.send_message(
                chat_id=chat_id,
                text=message
            )
