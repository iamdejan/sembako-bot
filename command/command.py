from abc import ABC, abstractclassmethod
from bot import BotProvider
from telegram import Bot


class Command(ABC):

    def __init__(self) -> None:
        self.bot = BotProvider.get()

    @abstractclassmethod
    def execute(self):
        pass
