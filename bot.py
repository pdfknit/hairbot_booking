import telebot
from telebot import types

from config import BOT_TOKEN
from keyboards import language_keyboard
from translations import TRANSLATIONS
from users import get_user_lang, set_user_lang, resolve_lang

bot = telebot.TeleBot(BOT_TOKEN)


def get_phrase(chat_id, key, **kwargs):
    lang = get_user_lang(chat_id)
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    chat_id = message.chat.id

    # set land, if it hasn't set yet
    if not get_user_lang(chat_id):
        resolve_lang(chat_id, user.language_code)

    name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    bot.send_message(chat_id, get_phrase(chat_id, "welcome", name=name))


@bot.message_handler(commands=['language'])
def handle_language(message):
    chat_id = message.chat.id
    kb, options = language_keyboard()
    bot.send_message(chat_id, get_phrase(chat_id, "choose_language"), reply_markup=kb)


@bot.message_handler(func=lambda msg: msg.text in ["🇬🇧 English", "🇷🇺 Русский", "🇵🇹 Português"])
def handle_language_selection(message):
    chat_id = message.chat.id
    text = message.text

    lang_code = {
        "🇬🇧 English": "en",
        "🇷🇺 Русский": "ru",
        "🇵🇹 Português": "pt"
    }.get(text, "en")

    set_user_lang(chat_id, lang_code)
    bot.send_message(chat_id, get_phrase(chat_id, "language_set"), reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
