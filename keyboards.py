from telebot import types
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