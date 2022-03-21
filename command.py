from abc import ABC, abstractclassmethod
from database import User
from markdown_builder.document import MarkdownDocument
from price import get_price_updates_for_users
from telegram import Bot


class Command(ABC):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @abstractclassmethod
    def execute(self):
        pass


class SubscribeCommand(Command):

    def __init__(self, bot: Bot, chat_id: int, name: str) -> None:
        super().__init__(bot)
        self.chat_id = chat_id
        self.name = name

    def execute(self):
        User.insert(id=self.chat_id,
                    name=self.name).on_conflict_replace().execute()
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Selamat! Anda sudah terdaftar."
        )


class UnsubscribeCommand(Command):

    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__(bot)
        self.chat_id = chat_id

    def execute(self):
        User.delete().where(User.id == self.chat_id).execute()
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Anda tidak terdaftar lagi."
        )


class PersonalUpdateCommand(Command):
    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__(bot)
        self.chat_id = chat_id

    def execute(self):
        get_price_updates_for_users(bot=self.bot, chat_ids=[self.chat_id])


class HelpCommand(Command):
    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__(bot)
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
        self.bot.send_message(chat_id=self.chat_id,
                              text=md.contents(), parse_mode="Markdown")
        md.close()


class UnknownCommand(Command):
    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__(bot)
        self.chat_id = chat_id

    def execute(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Perintah ini tidak diketahui. Silakan ketik `/help` untuk melihat daftar perintah.",
            parse_mode="Markdown"
        )
