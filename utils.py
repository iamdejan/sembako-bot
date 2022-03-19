from cgitb import text
from markdown_builder.document import MarkdownDocument
from telegram import Bot

def give_help(bot: Bot, chat_id: int):
    md = MarkdownDocument()
    md.append_text("Selamat datang di Sembako Bot! Ini adalah menu bantuan.")
    md.append_text("")
    md.append_text("Daftar perintah yang bisa digunakan:")
    md.append_text('`/register`: Untuk mendaftarkan akun Anda agar menerima update setiap malam.')
    md.append_text('`/unregister`: Untuk menarik akun Anda dari update otomatis.')
    md.append_text('`/help`: Untuk membuka menu bantuan.')
    bot.send_message(chat_id, text=md.contents())
    md.close()

def inform_unknown_command(bot: Bot, chat_id: int):
    bot.send_message(chat_id, text="Perintah ini tidak diketahui. Silakan ketik `/help` untuk melihat daftar perintah.")
