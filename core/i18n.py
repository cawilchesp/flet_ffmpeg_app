import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)

_translations = {}
_current_lang = "es"


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"theme": "light", "language": "es"}


def save_config(theme, language):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"theme": theme, "language": language}, f)
    except Exception:
        pass


def set_language(lang):
    global _current_lang
    _current_lang = lang
    if lang not in _translations:
        load_translations(lang)


def load_translations(lang):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locales_path = os.path.join(base_dir, "locales", f"{lang}.json")
    try:
        with open(locales_path, "r", encoding="utf-8") as f:
            _translations[lang] = json.load(f)
    except Exception:
        _translations[lang] = {}


def t(key):
    lang = _current_lang
    if lang not in _translations:
        load_translations(lang)
    return _translations.get(lang, {}).get(key, key)


def get_current_language():
    return _current_lang
