import firebase_admin
from firebase_admin import credentials, firestore
import os

if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(__file__), "firebase_credentials.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def set_user_lang(chat_id, lang_code):
    db.collection("users").document(str(chat_id)).set({
        "language": lang_code
    }, merge=True)

def get_user_lang(chat_id, fallback="en"):
    doc = db.collection("users").document(str(chat_id)).get()
    if doc.exists:
        return doc.to_dict().get("language", fallback)
    return fallback

def resolve_lang(chat_id, telegram_lang_code):
    """Установить язык пользователя (если ещё не установлен)"""
    existing_lang = get_user_lang(chat_id)
    if existing_lang:
        return existing_lang

    lang = telegram_lang_code if telegram_lang_code in ["en", "ru", "pt"] else "en"
    set_user_lang(chat_id, lang)
    return lang
