from command.command import Command
from markdown_builder.document import MarkdownDocument

class HelpCommand(Command):

    def __init__(self, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id

    def execute(self):
        md = MarkdownDocument()
        md.append_text(
            "Selamat datang di Sembako Bot! Ini adalah menu bantuan.")
        md.append_text("")
        md.append_text("Daftar perintah yang bisa digunakan:")
        md.append_text(
            '`/update`: Untuk mendapatkan harga terbaru sekarang, tanpa perlu daftar.')
        md.append_text(
            '`/subscribe`: Untuk mendaftarkan akun Anda agar menerima update setiap malam.')
        md.append_text(
            '`/unsubscribe`: Untuk menarik akun Anda dari update otomatis.')
        md.append_text('`/help`: Untuk membuka menu bantuan.')
        md.append_text('`/donate`: Untuk berdonasi.')
        self.bot.send_message(chat_id=self.chat_id,
                              text=md.contents(),
                              parse_mode="Markdown")
        md.close()
