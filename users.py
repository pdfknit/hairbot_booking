import json
import os

LANG_FILE = "user_lang.json"
SUPPORTED_LANGUAGES = ["en", "ru", "pt"]

# load existing user_lang or initialize empty
if os.path.exists(LANG_FILE):
    with open(LANG_FILE, "r", encoding="utf-8") as f:
        user_lang = json.load(f)
else:
    user_lang = {}

def save_lang():
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(user_lang, f, ensure_ascii=False, indent=2)

def get_user_lang(chat_id, fallback=None):
    return user_lang.get(str(chat_id), fallback)

def set_user_lang(chat_id, lang_code):
    user_lang[str(chat_id)] = lang_code
    save_lang()

def resolve_lang(chat_id, telegram_lang_code):
    """
    Determines and sets the user's language:
    1. If the user already exists → returns it
    2. If Telegram language is supported → sets and returns it
    3. Otherwise → sets and returns English
    """
    chat_id = str(chat_id)

    if chat_id in user_lang:
        return user_lang[chat_id]

    lang = telegram_lang_code if telegram_lang_code in SUPPORTED_LANGUAGES else "en"
    user_lang[chat_id] = lang
    save_lang()
    return lang