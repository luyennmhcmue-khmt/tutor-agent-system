import sqlite3
import hashlib
import random
import string
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tutor_system.db"

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        class_name TEXT,
        reset_code TEXT,
        strikes INTEGER DEFAULT 0,
        wrong_attempts INTEGER DEFAULT 0,
        is_locked INTEGER DEFAULT 0,
        ews_status TEXT DEFAULT 'Bình thường'
    );
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        seed_accounts(cur)
        conn.commit()
    conn.close()

def seed_accounts(cur):
    def_pw = hash_pw("123456")
    teachers = [
        ("gv_nam@thpt-nguyentrungtruc.edu.vn", "gv_nam@thpt-nguyentrungtruc.edu.vn", def_pw, "Thầy Nguyễn Hoàng Nam", "teacher", "Tổ Tin Học"),
        ("huong.le.informatics@gmail.com", "huong.le.informatics@gmail.com", def_pw, "Cô Lê Thị Thanh Hương", "teacher", "Tổ Tin Học"),
        ("tranminhduc.tin10@gmail.com", "tranminhduc.tin10@gmail.com", def_pw, "Thầy Trần Minh Đức", "teacher", "Tổ Tin Học")
    ]
    cur.executemany("INSERT INTO users (account_id, email, password_hash, full_name, role, class_name) VALUES (?, ?, ?, ?, ?, ?)", teachers)

    ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng"]
    dem = ["Văn", "Thị", "Minh", "Quốc", "Gia", "Thanh", "Đức", "Ngọc", "Bảo", "Hải"]
    ten = ["An", "Bình", "Châu", "Dũng", "Đạt", "Huy", "Khánh", "Linh", "Nam", "Phong", "Quân", "Thảo", "Trí", "Vy"]
    
    idx = 1
    students = []
    for c in range(1, 11):
        c_name = f"10A{c}"
        for s in range(1, 41):
            acc = f"10a{c}_{s:02d}"
            em = f"{acc}@student.school.edu.vn"
            name = f"{ho[idx % len(ho)]} {dem[(idx*3) % len(dem)]} {ten[(idx*7) % len(ten)]}"
            students.append((acc, em, def_pw, name, "student", c_name))
            idx += 1
    cur.executemany("INSERT INTO users (account_id, email, password_hash, full_name, role, class_name) VALUES (?, ?, ?, ?, ?, ?)", students)

def authenticate_user(acc_or_email, password):
    conn = get_connection()
    cur = conn.cursor()
    key = str(acc_or_email).strip().lower()
    
    # 1. Kiểm tra tài khoản đã tồn tại và đúng mật khẩu
    cur.execute("""
        SELECT * FROM users 
        WHERE (LOWER(account_id) = ? OR LOWER(email) = ?) AND password_hash = ?
    """, (key, key, hash_pw(password)))
    row = cur.fetchone()
    
    # 2. Nếu chưa có và là Email cá nhân -> Tự động kích hoạt tài khoản Giáo viên mới
    if not row and "@" in key:
        cur.execute("SELECT * FROM users WHERE LOWER(account_id) = ? OR LOWER(email) = ?", (key, key))
        exists = cur.fetchone()
        if not exists:
            # Tự động gán quyền Giáo viên bộ môn Tin học
            name_part = key.split("@")[0].replace(".", " ").title()
            default_fullname = f"Cô {name_part}" if "luyen" in key else f"Giáo viên ({name_part})"
            cur.execute("""
                INSERT INTO users (account_id, email, password_hash, full_name, role, class_name)
                VALUES (?, ?, ?, ?, 'teacher', 'Tổ Tin Học')
            """, (key, key, hash_pw(password), default_fullname))
            conn.commit()
            
            cur.execute("SELECT * FROM users WHERE LOWER(email) = ?", (key,))
            row = cur.fetchone()

    conn.close()
    return dict(row) if row else None

def change_user_password(account_id, old_pw, new_pw):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE account_id = ?", (account_id,))
    row = cur.fetchone()
    if not row or row["password_hash"] != hash_pw(old_pw):
        conn.close()
        return False, "Mật khẩu hiện tại không chính xác."
    cur.execute("UPDATE users SET password_hash = ? WHERE account_id = ?", (hash_pw(new_pw), account_id))
    conn.commit()
    conn.close()
    return True, "Đổi mật khẩu thành công!"

def generate_forgot_otp(identifier):
    conn = get_connection()
    cur = conn.cursor()
    key = str(identifier).strip().lower()
    cur.execute("SELECT account_id, email FROM users WHERE LOWER(account_id) = ? OR LOWER(email) = ?", (key, key))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None, "Không tìm thấy thông tin tài khoản trên hệ thống."
    otp = ''.join(random.choices(string.digits, k=6))
    cur.execute("UPDATE users SET reset_code = ? WHERE account_id = ?", (otp, row["account_id"]))
    conn.commit()
    conn.close()
    return otp, row["email"]

def reset_password_with_otp(identifier, otp, new_pw):
    conn = get_connection()
    cur = conn.cursor()
    key = str(identifier).strip().lower()
    cur.execute("SELECT account_id, reset_code FROM users WHERE LOWER(account_id) = ? OR LOWER(email) = ?", (key, key))
    row = cur.fetchone()
    if not row or str(row["reset_code"]).strip() != str(otp).strip():
        conn.close()
        return False, "Mã OTP không hợp lệ hoặc đã hết hạn."
    cur.execute("UPDATE users SET password_hash = ?, reset_code = NULL WHERE account_id = ?", (hash_pw(new_pw), row["account_id"]))
    conn.commit()
    conn.close()
    return True, "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập ngay."

def get_user_by_account_id(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE account_id = ?", (str(account_id).strip().lower(),))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_status(account_id, strikes, wrong, is_locked, ews_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET strikes = ?, wrong_attempts = ?, is_locked = ?, ews_status = ? WHERE account_id = ?",
                (strikes, wrong, 1 if is_locked else 0, ews_status, str(account_id).strip().lower()))
    conn.commit()
    conn.close()

def unlock_user_account(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_locked = 0, strikes = 0, wrong_attempts = 0, ews_status = 'Bình thường' WHERE account_id = ?",
                (str(account_id).strip().lower(),))
    conn.commit()
    conn.close()

# Đồng bộ bí danh tên hàm tương thích mọi phiên bản
change_password = change_user_password
create_password_reset_code = generate_forgot_otp
reset_password_with_code = reset_password_with_otp
get_user_status = get_user_by_account_id
get_user_by_username = get_user_by_account_id
update_student_progress = update_user_status
update_student_status = update_user_status
unlock_account = unlock_user_account
unlock_student_account = unlock_user_account