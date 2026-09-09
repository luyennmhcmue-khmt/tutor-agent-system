import re
import unicodedata

LEET_MAP = {
    '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b',
    '@': 'a', '$': 's', '!': 'i', '*': '', '.': '', '-': '', '_': '', ' ': ''
}

PROFANITY_PATTERNS = [
    r'(d|đ)[iieeyy]*[m|p][eeyy]*', r'(d|đ)[iieeyy]*t+[ ]*m[eeyy]*', r'(d|đ)u+[ ]*m[aaoo]*',
    r'd(c|k)m', r'dmm+', r'cai*[ ]*l[oouu*0-9]+n', r'l[oouu*0-9]+n', r'clgt',
    r'con[ ]*c(a|ă|â)*c', r'c(a|ă|â)+k', r'c(a|ă|â)+x', r'\bcc\b',
    r'con[ ]*ch[oóòõọ]+', r'ch[oóòõọ]+[ ]*d[eéèẽẹ]+', r'oc[ ]*ch[oóòõọ]+', r'suc[ ]*vat',
    r'v(c|k)l+', r'\bvl\b', r'v(a|ã)i+[ ]*(l|c|ch)', r'(d|đ)(e|é)+o+', r'd(e|e)l+',
    r'b+i+t+c+h+', r'f+u+c+k+', r's+h+i+t+', r'c+u+n+t+'
]
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in PROFANITY_PATTERNS]

def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn').replace('đ', 'd')
    chars = [LEET_MAP.get(c, c) for c in text]
    return re.sub(r'(.)\1{2,}', r'\1\1', ''.join(chars))

def check_profanity(raw_text: str) -> tuple[bool, str | None]:
    clean = normalize_text(raw_text)
    for pattern in COMPILED_PATTERNS:
        match = pattern.search(clean)
        if match:
            return True, match.group()
    return False, None