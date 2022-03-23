from dotenv import load_dotenv
from telegram import Bot
from typing import Optional

import os

load_dotenv()


class BotProvider:
    bot: Optional[Bot] = None

    @staticmethod
    def get() -> Optional[Bot]:
        if BotProvider.bot is None:
            BotProvider.bot = Bot(token=os.getenv("API_KEY").__str__())
        return BotProvider.bot
