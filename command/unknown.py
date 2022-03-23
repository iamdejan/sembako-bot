from command.command import Command

class UnknownCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Perintah ini tidak diketahui. Silakan ketik `/help` untuk melihat daftar perintah.",
            parse_mode="Markdown"
        )
