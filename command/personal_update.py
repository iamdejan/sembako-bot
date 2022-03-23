from command.command import Command
from price import get_price_updates_for_users

class PersonalUpdateCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        get_price_updates_for_users(bot=self.bot, chat_ids=[self.chat_id])
