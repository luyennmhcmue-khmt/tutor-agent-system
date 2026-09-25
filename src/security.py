import os
import json
import re
from datetime import datetime

VIOLATIONS_FILE = os.path.join("data", "user_violations.json")

# Danh mục từ khóa kiểm duyệt học đường
PROFANITY_PATTERNS = [
    r"\bđm\b", r"\bdm\b", r"\bvcl\b", r"\bvl\b", r"\bchó\b", r"\bngu\b",
    r"\bcút\b", r"\bđụ\b", r"\bmẹ mày\b", r"\bdcm\b", r"\bclmm\b",
    r"\bđéo\b", r"\bdeo\b", r"\bcc\b", r"\bloz\b", r"\blồn\b",
    r"\bcac\b", r"\bcặc\b"
]

def _ensure_storage():
    """Tự động tạo thư mục và tệp JSON nếu chưa tồn tại."""
    os.makedirs(os.path.dirname(VIOLATIONS_FILE), exist_ok=True)
    if not os.path.exists(VIOLATIONS_FILE):
        with open(VIOLATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def check_profanity(text: str) -> bool:
    """Kiểm tra từ ngữ thô tục."""
    if not text:
        return False
    t = text.lower()
    return any(re.search(pat, t) for pat in PROFANITY_PATTERNS)

def get_user_status(username: str) -> dict:
    """Đọc trạng thái kỷ luật trực tiếp từ ổ cứng."""
    _ensure_storage()
    try:
        with open(VIOLATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, {"strikes": 0, "locked": False, "history": []})
    except Exception:
        return {"strikes": 0, "locked": False, "history": []}

def record_violation(username: str, prompt_text: str) -> tuple[int, bool]:
    """
    Ghi nhận vi phạm vĩnh viễn vào file JSON.
    Trả về: (số lần vi phạm, trạng thái tài khoản bị khóa)
    """
    _ensure_storage()
    try:
        with open(VIOLATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    user_info = data.get(username, {"strikes": 0, "locked": False, "history": []})
    
    if user_info.get("locked", False):
        return user_info["strikes"], True

    user_info["strikes"] += 1
    user_info.setdefault("history", []).append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strike": user_info["strikes"],
        "prompt": prompt_text
    })

    # Đạt mốc 3 lần -> Khóa cứng vĩnh viễn
    if user_info["strikes"] >= 3:
        user_info["locked"] = True
        user_info["locked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data[username] = user_info
    with open(VIOLATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return user_info["strikes"], user_info["locked"]

def unlock_account(username: str) -> bool:
    """Giáo viên mở khóa tài khoản."""
    _ensure_storage()
    try:
        with open(VIOLATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if username in data:
            data[username]["locked"] = False
            data[username]["strikes"] = 0
            with open(VIOLATIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
    except Exception:
        pass
    return False

def get_all_locked_accounts() -> list:
    """Lấy danh sách tất cả học sinh đang bị khóa để GV quản lý."""
    _ensure_storage()
    try:
        with open(VIOLATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [acc for acc, info in data.items() if info.get("locked")]
    except Exception:
        return []