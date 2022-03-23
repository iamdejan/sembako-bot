from command.command import Command
from database import User

class UnsubscribeCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        User.delete().where(User.id == self.chat_id).execute()
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Anda tidak terdaftar lagi."
        )
