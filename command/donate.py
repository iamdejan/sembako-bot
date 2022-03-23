from command.command import Command
from markdown_builder.document import MarkdownDocument

class DonateCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        md = MarkdownDocument()
        md.append_text("Anda bisa berdonasi melalui beberapa platform:")
        md.append_text("- Bank Jago: `1095 1517 0227` (nomor rekening) atau `gdejan1998` (Jago ID untuk sesama pemilik rekening Jago)")
        self.bot.send_message(chat_id=self.chat_id,
                              text=md.contents(),
                              parse_mode="Markdown")
        md.close()
