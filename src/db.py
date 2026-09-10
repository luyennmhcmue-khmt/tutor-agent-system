import sqlite3
from pathlib import Path
import hashlib
import random
import re
from datetime import datetime, timedelta

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "educoder10.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()

def _generate_student_name(class_num: int, std_num: int) -> str:
    """Tạo họ và tên tiếng Việt thực tế, chuẩn danh sách học sinh THPT."""
    ho_list = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương"]
    lot_nam = ["Văn", "Minh", "Hoàng", "Đức", "Hữu", "Tuấn", "Quốc", "Đình", "Quang", "Gia"]
    ten_nam = ["An", "Bình", "Cường", "Dũng", "Đạt", "Hải", "Hiếu", "Huy", "Khang", "Khoa", "Long", "Nam", "Nghĩa", "Phúc", "Quân", "Sơn", "Thịnh", "Trí", "Trung", "Tùng", "Vinh"]
    lot_nu = ["Thị", "Mai", "Phương", "Ngọc", "Thảo", "Khánh", "Quỳnh", "Thanh", "Cẩm", "Như"]
    ten_nu = ["Anh", "Châu", "Giang", "Hà", "Hân", "Hoa", "Lan", "Linh", "Mai", "My", "Nga", "Ngân", "Ngọc", "Nhung", "Oanh", "Phương", "Quỳnh", "Thảo", "Trang", "Trúc", "Vy", "Yến"]

    seed_val = class_num * 100 + std_num
    ho = ho_list[seed_val % len(ho_list)]
    if std_num % 2 == 1:
        lot = lot_nam[(seed_val // 3) % len(lot_nam)]
        ten = ten_nam[(seed_val // 7) % len(ten_nam)]
    else:
        lot = lot_nu[(seed_val // 3) % len(lot_nu)]
        ten = ten_nu[(seed_val // 7) % len(ten_nu)]
    return f"{ho} {lot} {ten}"

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Bảng Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'teacher')),
        class_name TEXT DEFAULT '10A1',
        strikes INTEGER DEFAULT 0,
        wrong_attempts INTEGER DEFAULT 0,
        is_locked INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Bình thường'
    );
    """)

    # 2. Bảng Submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id TEXT,
        exercise_id TEXT,
        user_email TEXT,
        exercise_code TEXT,
        score REAL NOT NULL,
        status TEXT NOT NULL,
        verdict TEXT DEFAULT 'WA',
        submitted_code TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Bảng OTP
    cur.execute("""
    CREATE TABLE IF NOT EXISTS otps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id TEXT NOT NULL,
        otp_code TEXT NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        is_used INTEGER DEFAULT 0
    );
    """)

    # --- TỰ ĐỘNG BỔ SUNG CỘT CÒN THIẾU TRONG BẢNG USERS ---
    cur.execute("PRAGMA table_info(users)")
    user_cols = [col[1] for col in cur.fetchall()]
    for col_name, col_type in {
        "account_id": "TEXT", "strikes": "INTEGER DEFAULT 0",
        "wrong_attempts": "INTEGER DEFAULT 0", "is_locked": "INTEGER DEFAULT 0",
        "status": "TEXT DEFAULT 'Bình thường'", "class_name": "TEXT DEFAULT '10A1'"
    }.items():
        if col_name not in user_cols:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
            except Exception:
                pass

    # --- TỰ ĐỘNG BỔ SUNG CỘT CÒN THIẾU TRONG BẢNG SUBMISSIONS (Xử lý dứt điểm lỗi status) ---
    cur.execute("PRAGMA table_info(submissions)")
    sub_cols = [col[1] for col in cur.fetchall()]
    for col_name, col_type in {
        "account_id": "TEXT", "exercise_id": "TEXT",
        "user_email": "TEXT", "exercise_code": "TEXT",
        "status": "TEXT DEFAULT 'Accepted (AC)'",
        "verdict": "TEXT DEFAULT 'AC'"
    }.items():
        if col_name not in sub_cols:
            try:
                cur.execute(f"ALTER TABLE submissions ADD COLUMN {col_name} {col_type};")
            except Exception:
                pass

    default_pw = hash_pw("123456")

    # Tạo tài khoản giáo viên mặc định
    cur.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher'")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (account_id, email, password_hash, full_name, role, class_name)
            VALUES ('gv_admin', 'giaovien@gmail.com', ?, 'Thầy/Cô Quản Trị', 'teacher', 'Tổ Tin Học')
        """, (default_pw,))
    cur.execute("UPDATE users SET full_name = REPLACE(REPLACE(REPLACE(full_name, 'Cô ', ''), 'Thầy ', ''), 'Thầy/Cô ', '') WHERE role = 'teacher'")
    conn.commit()
    # Khởi tạo hoặc cập nhật HỌ VÀ TÊN THẬT cho 450 học sinh (10 lớp từ 10A1 đến 10A10, mỗi lớp 45 em)
    for c in range(1, 11):
        class_name = f"10A{c}"
        for s in range(1, 46):
            acc_id = f"10a{c}_{s:02d}"
            real_name = _generate_student_name(c, s)
            email = f"{acc_id}@student.edu.vn"

            cur.execute("SELECT id, full_name FROM users WHERE LOWER(account_id) = ?", (acc_id,))
            existing_user = cur.fetchone()

            if not existing_user:
                cur.execute("""
                    INSERT INTO users (account_id, email, password_hash, full_name, role, class_name)
                    VALUES (?, ?, ?, ?, 'student', ?)
                """, (acc_id, email, default_pw, real_name, class_name))
            elif "Học sinh" in existing_user["full_name"]:
                # Đổi các tên giữ chỗ cũ sang họ tên thật
                cur.execute("UPDATE users SET full_name = ?, class_name = ? WHERE id = ?", (real_name, class_name, existing_user["id"]))

    conn.commit()
    conn.close()

init_database = init_db

def authenticate_user(acc_or_email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    key = str(acc_or_email).strip().lower()
    pw_h = hash_pw(password)
    
    cur.execute("""
        SELECT * FROM users 
        WHERE (LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?) AND password_hash = ?
    """, (key, key, pw_h))
    row = cur.fetchone()

    # Giáo viên đăng nhập bằng Gmail bất kỳ
    if not row and "@" in key:
        cur.execute("SELECT * FROM users WHERE LOWER(email) = ?", (key,))
        if not cur.fetchone():
            name_part = key.split("@")[0].replace(".", " ").title()
            fullname = f"Thầy/Cô ({name_part})"
            cur.execute("""
                INSERT INTO users (account_id, email, password_hash, full_name, role, class_name)
                VALUES (?, ?, ?, ?, 'teacher', 'Tổ Tin Học')
            """, (key, key, pw_h, fullname))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE LOWER(email) = ?", (key,))
            row = cur.fetchone()

    # Tự động cấp nếu học sinh gõ đúng định dạng 10aX_YY
    if not row:
        m = re.match(r"^10a(\d+)_(\d+)$", key)
        if m and pw_h == hash_pw("123456"):
            c_num = int(m.group(1))
            s_num = int(m.group(2))
            c_name = f"10A{c_num}"
            fullname = _generate_student_name(c_num, s_num)
            cur.execute("""
                INSERT OR IGNORE INTO users (account_id, email, password_hash, full_name, role, class_name)
                VALUES (?, ?, ?, ?, 'student', ?)
            """, (key, f"{key}@student.edu.vn", pw_h, fullname, c_name))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE LOWER(account_id) = ?", (key,))
            row = cur.fetchone()

    conn.close()
    if not row:
        return None, "Tên tài khoản hoặc mật khẩu không chính xác."
    
    user_dict = dict(row)
    if user_dict.get("is_locked") == 1:
        return None, "🚫 Tài khoản đã bị khóa do vi phạm quy chế học tập."
        
    return user_dict, "Đăng nhập thành công!"

def get_student_highest_score(account_id: str, exercise_id: str) -> float:
    if not account_id:
        return 0.0
    conn = get_connection()
    cur = conn.cursor()
    target_acc = str(account_id).strip().lower()
    target_ex = str(exercise_id).strip().upper()
    val = 0.0
    try:
        cur.execute("PRAGMA table_info(submissions)")
        cols = [c[1] for c in cur.fetchall()]
        if "account_id" in cols and "exercise_id" in cols:
            cur.execute("""
                SELECT MAX(score) FROM submissions 
                WHERE (LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(user_email, '')) = ?) 
                  AND (UPPER(COALESCE(exercise_id, '')) = ? OR UPPER(COALESCE(exercise_code, '')) = ?)
            """, (target_acc, target_acc, target_ex, target_ex))
            row = cur.fetchone()
            if row and row[0] is not None:
                val = float(row[0])
        elif "user_email" in cols and "exercise_code" in cols:
            cur.execute("""
                SELECT MAX(score) FROM submissions 
                WHERE LOWER(user_email) = ? AND UPPER(exercise_code) = ?
            """, (target_acc, target_ex))
            row = cur.fetchone()
            if row and row[0] is not None:
                val = float(row[0])
    except Exception:
        val = 0.0
    finally:
        conn.close()
    return val

def save_submission(account_id: str, exercise_id: str, score: float, status: str, code: str):
    """Lưu bài nộp thích ứng linh hoạt theo các cột thực tế của bảng."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(submissions)")
    cols = [c[1] for c in cur.fetchall()]
    
    data = {
        "account_id": str(account_id),
        "exercise_id": str(exercise_id),
        "user_email": str(account_id),
        "exercise_code": str(exercise_id),
        "score": float(score),
        "status": str(status),
        "verdict": "AC" if ("Accepted" in str(status) or "AC" in str(status)) else "WA",
        "submitted_code": str(code)
    }
    
    insert_cols = [k for k in data.keys() if k in cols]
    placeholders = ", ".join(["?"] * len(insert_cols))
    col_names = ", ".join(insert_cols)
    values = [data[k] for k in insert_cols]
    
    cur.execute(f"INSERT INTO submissions ({col_names}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def change_user_password(account_id: str, old_pw: str, new_pw: str):
    conn = get_connection()
    cur = conn.cursor()
    target = str(account_id).strip().lower()
    cur.execute("SELECT password_hash FROM users WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?", (target, target))
    row = cur.fetchone()
    if not row or row["password_hash"] != hash_pw(old_pw):
        conn.close()
        return False, "Mật khẩu hiện tại không chính xác."
    
    cur.execute("UPDATE users SET password_hash = ? WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?",
                (hash_pw(new_pw), target, target))
    conn.commit()
    conn.close()
    return True, "Đổi mật khẩu thành công!"

def unlock_user_account(account_id: str):
    conn = get_connection()
    cur = conn.cursor()
    target = str(account_id).strip().lower()
    cur.execute("""
        UPDATE users 
        SET strikes = 0, wrong_attempts = 0, is_locked = 0, status = 'Bình thường'
        WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?
    """, (target, target))
    conn.commit()
    conn.close()
    return True

def generate_forgot_otp(account_or_email: str):
    conn = get_connection()
    cur = conn.cursor()
    target = str(account_or_email).strip().lower()

    cur.execute("SELECT * FROM users WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?", (target, target))
    row = cur.fetchone()

    if not row and "@" in target:
        name_part = target.split("@")[0].replace(".", " ").title()
        cur.execute("""
            INSERT INTO users (account_id, email, password_hash, full_name, role, class_name)
            VALUES (?, ?, ?, ?, 'teacher', 'Tổ Tin Học')
        """, (target, target, hash_pw("123456"), f"Thầy/Cô ({name_part})"))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE LOWER(email) = ?", (target,))
        row = cur.fetchone()

    if not row:
        conn.close()
        return None, None, "Không tìm thấy tài khoản hoặc email trên hệ thống."

    user_data = dict(row)
    dest_email = user_data.get("email") or target
    otp = f"{random.randint(100000, 999999)}"
    expires_at = datetime.now() + timedelta(minutes=3)

    cur.execute("INSERT INTO otps (account_id, otp_code, expires_at) VALUES (?, ?, ?)",
                (user_data["account_id"] or dest_email, otp, expires_at))
    conn.commit()
    conn.close()

    try:
        from src.utils.mailer import send_real_otp_email
        sent_ok, send_msg = send_real_otp_email(dest_email, otp)
        return otp, dest_email, send_msg
    except Exception:
        return otp, dest_email, f"Mã OTP là {otp} (có hiệu lực 3 phút)"

def reset_password_with_otp(account_or_email: str, otp_entered: str, new_password: str):
    conn = get_connection()
    cur = conn.cursor()
    target = str(account_or_email).strip().lower()

    cur.execute("""
        SELECT * FROM otps 
        WHERE (LOWER(account_id) = ? OR LOWER(account_id) = ?) AND otp_code = ? AND is_used = 0 
        ORDER BY id DESC LIMIT 1
    """, (target, target, otp_entered.strip()))
    rec = cur.fetchone()

    if not rec:
        conn.close()
        return False, "Mã OTP không đúng hoặc đã qua sử dụng."

    cur.execute("UPDATE users SET password_hash = ? WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?",
                (hash_pw(new_password), target, target))
    cur.execute("UPDATE otps SET is_used = 1 WHERE id = ?", (rec["id"],))
    conn.commit()
    conn.close()
    return True, "Cập nhật mật khẩu thành công!"
def update_user_fullname(account_id: str, new_fullname: str):
    return True
def add_user_strike(user_identifier: str) -> tuple[int, bool]:
    """Ghi nhận vi phạm ngôn từ. Đủ 3 lần khóa tài khoản ngay lập tức."""
    conn = get_connection()
    cur = conn.cursor()
    key = str(user_identifier).strip().lower()

    cur.execute("""
        SELECT id, strikes, is_locked FROM users 
        WHERE LOWER(COALESCE(account_id, '')) = ? 
           OR LOWER(COALESCE(email, '')) = ? 
           OR CAST(id AS TEXT) = ?
    """, (key, key, key))
    row = cur.fetchone()

    if not row:
        conn.close()
        return 1, False

    uid = row["id"]
    current_strikes = (row["strikes"] or 0) + 1
    is_locked = 1 if current_strikes >= 3 else 0
    status_str = "Bị khóa do vi phạm kỷ luật" if is_locked else f"Cảnh cáo ({current_strikes}/3)"

    cur.execute("""
        UPDATE users 
        SET strikes = ?, is_locked = ?, status = ? 
        WHERE id = ?
    """, (current_strikes, is_locked, status_str, uid))
    conn.commit()
    conn.close()

    return current_strikes, bool(is_locked)

    current_strikes = (row["strikes"] or 0) + 1
    is_locked = 1 if current_strikes >= 3 else 0
    status = "Bị khóa do vi phạm kỷ luật" if is_locked else f"Cảnh cáo ({current_strikes}/3)"

    cur.execute("""
        UPDATE users 
        SET strikes = ?, is_locked = ?, status = ?
        WHERE LOWER(COALESCE(account_id, '')) = ? OR LOWER(COALESCE(email, '')) = ?
    """, (current_strikes, is_locked, status, target, target))
    conn.commit()
    conn.close()
    return current_strikes, bool(is_locked)