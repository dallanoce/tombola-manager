from .translations import TRANSLATIONS

class LanguageManager:
    _instance = None
    _current_language = 'en'  # Default language

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_text(cls, key, *args):
        """Get translated text for the given key"""
        try:
            text = TRANSLATIONS[cls._current_language][key]
            if args:
                return text.format(*args)
            return text
        except KeyError:
            return f"Missing translation: {key}"

    @classmethod
    def set_language(cls, language):
        """Set the current language (en/it)"""
        if language in TRANSLATIONS:
            cls._current_language = language
            return True
        return False

    @classmethod
    def get_current_language(cls):
        """Get the current language code"""
        return cls._current_language