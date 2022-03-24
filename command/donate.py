from command.command import Command
from markdown_builder.document import MarkdownDocument


class DonateCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        md: MarkdownDocument = MarkdownDocument()
        md.append_text("Anda bisa berdonasi melalui beberapa platform:")
        self.bot.send_message(chat_id=self.chat_id,
                              text=md.contents(),
                              parse_mode="Markdown")
        md.close()

        wallets: dict = [
            {
                "provider": "GoPay",
                "is_qr": True,
                "url": "https://user-images.githubusercontent.com/15686093/159909557-fdcaa8d5-374e-454f-8d48-c139f12f2456.png"
            },
            {
                "provider": "DANA",
                "is_qr": True,
                "url": "https://user-images.githubusercontent.com/15686093/159909522-39de7788-93e0-4c56-ad74-c140c34b5bf4.png"
            },
            {
                "provider": "OVO",
                "is_qr": True,
                "url": "https://user-images.githubusercontent.com/15686093/159909611-7e55a5d1-1906-4b39-9439-01928f70475c.png"
            },
            {
                "provider": "LinkAja",
                "is_qr": True,
                "url": "https://user-images.githubusercontent.com/15686093/159909589-d7289930-8d6d-4b8e-8ec4-c22d95a8c22b.png"
            },
            {
                "provider": "Bank Jago",
                "is_qr": False,
                "text": "`1095 1517 0227` (nomor rekening) atau `gdejan1998` (Jago ID untuk sesama pemilik rekening Jago)"
            }
        ]

        for wallet in wallets:
            if wallet["is_qr"]:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    disable_web_page_preview=False,
                    parse_mode="Markdown",
                    text=f'[{wallet["provider"]}]({wallet["url"]})'
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id, text=f'{wallet["provider"]}: {wallet["text"]}', parse_mode="Markdown")
