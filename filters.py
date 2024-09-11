import re

# Словарь заменяемых символов (замены букв на похожие символы)
CHAR_REPLACEMENTS = {
    'а': '[аa@]', 'б': '[бb6]', 'в': '[вv]', 'г': '[гg]', 'д': '[дd]',
    'е': '[еe3]', 'ё': '[ёe]', 'ж': '[жzh]', 'з': '[зz3]', 'и': '[иi1!]',
    'й': '[йi1]', 'к': '[кk]', 'л': '[лl]', 'м': '[мm]', 'н': '[нh]',
    'о': '[оo0(){}<>]', 'п': '[пn]', 'р': '[рp]', 'с': '[сc]', 'т': '[тt]',
    'у': '[уy]', 'ф': '[фf]', 'х': '[хx]', 'ц': '[цc]', 'ч': '[чch4]',
    'ш': '[шsh]', 'щ': '[щsch]', 'ы': '[ыy]', 'э': '[эe]', 'ю': '[юyu]',
    'я': '[яya]', ' ': r'\s*'
}

# Расширенный список запрещённых слов и фраз
FORBIDDEN_WORDS = [
    # ... (список слов)
]

FORBIDDEN_PHRASES = [
    # ... (список фраз)
]

# Регулярное выражение для поиска ссылок
URL_REGEX = r'(https?://\S+|t\.me/\S+)'

def normalize_word(word):
    normalized = word.lower()
    for char, replacement in CHAR_REPLACEMENTS.items():
        normalized = normalized.replace(char, replacement)
    return normalized

def contains_forbidden_word(text):
    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        pattern = normalize_word(word)
        if re.search(pattern, text_lower):
            return True
    return False

def contains_forbidden_phrase(text):
    text_lower = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        pattern = normalize_word(phrase)
        if re.search(pattern, text_lower):
            return True
    return False

