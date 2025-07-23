import re
from datetime import datetime

import telebot
from telebot import types

from config import BOT_TOKEN
from keyboards import language_keyboard, slot_choice_keyboard, slots_keyboard, main_menu_keyboard, confirm_keyboard
from translations import TRANSLATIONS
from users import get_user_lang, set_user_lang, resolve_lang
from calendar_api import get_free_slots, find_nearest_slots, book_slot

bot = telebot.TeleBot(BOT_TOKEN)
pending_bookings = {}  # chat_id -> (date, time)


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

    bot.send_message(
        chat_id,
        get_phrase(chat_id, "confirm_save_profile"),
        reply_markup=confirm_keyboard(chat_id)
    )


@bot.message_handler(commands=['language'])
def handle_language(message):
    chat_id = message.chat.id
    kb, options = language_keyboard()
    bot.send_message(chat_id, get_phrase(chat_id, "choose_language"), reply_markup=kb)


@bot.message_handler(commands=["book"])
def handle_slots(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, get_phrase(chat_id, "slots_prompt"), reply_markup=slot_choice_keyboard(chat_id))


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




@bot.message_handler(func=lambda msg: msg.text in ["Nearest available", "Ближайшее время", "Horários mais próximos"])
def handle_nearest_slot(message):
    chat_id = message.chat.id
    slots = find_nearest_slots()

    if not slots:
        bot.send_message(chat_id, get_phrase(chat_id, "no_slots_found"))
        return

    bot.send_message(
        chat_id,
        get_phrase(chat_id, "choose_slot"),
        reply_markup=slots_keyboard(slots)
    )


@bot.message_handler(func=lambda msg: re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", msg.text))
def handle_slot_selection(message):
    chat_id = message.chat.id
    selected = message.text
    date, time = selected.split()
    pending_bookings[chat_id] = (date, time)

    bot.send_message(
        chat_id,
        get_phrase(chat_id, "confirm_slot", date=date, time=time),
        reply_markup=confirm_keyboard(chat_id)
    )


@bot.message_handler(func=lambda msg: msg.text)
def handle_confirmation(message):
    chat_id = message.chat.id
    text = message.text
    lang = get_user_lang(chat_id)
    username = message.username or ""

    cancel_text = TRANSLATIONS[lang].get("cancel_button", "❌ Cancel")
    confirm_text = TRANSLATIONS[lang].get("confirm_button", "✅ Yes")

    if text == cancel_text:
        bot.send_message(chat_id, get_phrase(chat_id, "booking_cancelled"), reply_markup=main_menu_keyboard(chat_id))
        pending_bookings.pop(chat_id, None)
        return

    if text == confirm_text:
        if chat_id not in pending_bookings:
            bot.send_message(chat_id, get_phrase(chat_id, "no_pending_booking"), reply_markup=main_menu_keyboard(chat_id))
            return

        date, time = pending_bookings.pop(chat_id)
        user = message.from_user
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()

        success = book_slot(date, time, name, "Hair Service", username=username, phone="")
        if success:
            bot.send_message(chat_id, get_phrase(chat_id, "booking_confirmed", date=date, time=time), reply_markup=main_menu_keyboard(chat_id))
        else:
            bot.send_message(chat_id, get_phrase(chat_id, "slot_taken", date=date, time=time), reply_markup=main_menu_keyboard(chat_id))




if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
