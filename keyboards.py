from telebot import types

from translations import TRANSLATIONS
from users import get_user_lang


def language_keyboard():
    """Returns language selection keyboard and a lookup dict"""
    options = {
        "🇬🇧 English": "en",
        "🇷🇺 Русский": "ru",
        "🇵🇹 Português": "pt"
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for label in options:
        markup.add(label)

    return markup, options


def main_menu_keyboard(chat_id):
    """main menu"""
    lang = get_user_lang(chat_id)

    buttons = {
        "en": ["💇 Book Appointment", "⚙️ Settings"],
        "ru": ["💇 Записаться", "⚙️ Настройки"],
        "pt": ["💇 Marcar horário", "⚙️ Configurações"]
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for label in buttons.get(lang, buttons["en"]):
        markup.add(label)

    return markup


def cancel_keyboard(chat_id):
    """cancel button"""
    lang = get_user_lang(chat_id)
    cancel_labels = {
        "en": "❌ Cancel",
        "ru": "❌ Отмена",
        "pt": "❌ Cancelar"
    }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(cancel_labels.get(lang, "❌ Cancel"))
    return markup


def slot_choice_keyboard(chat_id):
    """Keyboard to choose slot search method"""
    lang = get_user_lang(chat_id)

    buttons = {
        "en": ["Choose by date", "Nearest available"],
        "ru": ["Выбрать дату", "Ближайшее время"],
        "pt": ["Escolher data", "Próximo horário disponível"]
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for label in buttons.get(lang, buttons["en"]):
        markup.add(label)

    return markup


def slots_keyboard(slots: list):
    """Keyboard with available slots like '2025-08-05 12:00'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for date, time in slots:
        label = f"{date} {time}"
        markup.add(label)
    return markup

def confirm_keyboard(chat_id):
    """Returns localized confirmation keyboard"""
    lang = get_user_lang(chat_id)
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    confirm = lang_dict.get("confirm_button", "✅ Yes")
    cancel = lang_dict.get("cancel_button", "❌ Cancel")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(confirm, cancel)
    return markup

