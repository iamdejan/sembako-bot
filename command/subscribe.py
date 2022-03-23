from command.command import Command
from database import User

class SubscribeCommand(Command):

    def __init__(self, chat_id: int, name: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.name = name

    def execute(self):
        User.insert(id=self.chat_id,
                    name=self.name).on_conflict_replace().execute()
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Selamat! Anda sudah terdaftar."
        )
