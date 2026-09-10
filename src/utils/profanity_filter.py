import re
import unicodedata

BAD_WORDS = [
    "khung", "khùng", "dien", "điên", "óc chó", "oc cho", "óc lợn", "oc lon",
    "đồ ngu", "do ngu", "ngu vcl", "ngu vl", "thằng khùng", "thang khung", 
    "con điên", "con dien", "bị điên", "bi dien", "mẹ mày", "me may", 
    "con chó", "con cho", "đồ chó", "do cho", "chó chết", "cút", "biến đi"
]

ACRONYMS = ["clmm", "clm", "cdmm", "cmm", "dmm", "đmm", "dm", "đm", "dcm", "đcm", "vcl", "vkl", "vcc", "đkm", "dkm", "cc"]

SAFE_WORDS = ["luôn", "luon", "lớn", "lon nước", "nilon", "khuôn", "buồn", "uống"]

def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).replace("đ", "d").replace("Đ", "D")

def check_profanity(text: str) -> tuple[bool, str]:
    if not text:
        return False, ""
    
    raw = text.lower().strip()
    no_acc = strip_accents(raw)

    # Nếu câu có chứa từ an toàn hợp lệ, không xét phạt nhầm
    for sw in SAFE_WORDS:
        if sw in raw:
            raw = raw.replace(sw, " ")
            no_acc = no_acc.replace(strip_accents(sw), " ")

    for bad in BAD_WORDS:
        bad_no_acc = strip_accents(bad)
        pattern = r'\b' + re.escape(bad) + r'\b'
        pattern_no_acc = r'\b' + re.escape(bad_no_acc) + r'\b'
        if re.search(pattern, raw) or re.search(pattern_no_acc, no_acc):
            return True, bad

    words = re.findall(r'[a-zA-Z0-9_]+', raw)
    for w in words:
        if w in ACRONYMS:
            return True, w

    return False, ""