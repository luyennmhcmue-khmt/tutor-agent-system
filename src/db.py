import os
import random
import sqlite3

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "database.db")

# Định nghĩa chuẩn 5 nhóm năng lực và số lượng bài thực tế tương ứng
TOPIC_CONFIG = {
    "C1": {"name": "Vào/Ra & Biến cơ sở (Bài 16-18)", "total_ex": 3},
    "C2": {"name": "Rẽ nhánh & Vòng lặp (Bài 19-21)", "total_ex": 3},
    "C3": {"name": "Xâu ký tự & Kiểu List (Bài 22-25)", "total_ex": 2},
    "C4": {"name": "Hàm & Chương trình con (Bài 26-28)", "total_ex": 1},
    "C5": {"name": "Thuật toán & Gỡ lỗi (Bài 29-30)", "total_ex": 1}
}

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Bảng tài khoản
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            class_name TEXT,
            strikes INTEGER DEFAULT 0,
            is_locked INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Bình thường'
        )
    """)
    
    # 2. Bảng lưu trữ bài nộp thực tế
    cur.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT,
            exercise_id TEXT,
            code TEXT,
            status TEXT,
            score REAL DEFAULT 0,
            misconception TEXT DEFAULT '',
            attempt_count INTEGER DEFAULT 1,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Bảng Ma trận năng lực thực tế
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_competencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT,
            topic_prefix TEXT,
            topic_name TEXT,
            mastery_percent REAL DEFAULT 0.0,
            total_attempts INTEGER DEFAULT 0,
            passed_count INTEGER DEFAULT 0,
            last_misconception TEXT DEFAULT 'Chưa có',
            UNIQUE(account_id, topic_prefix)
        )
    """)

    # TỰ ĐỘNG MIGRATION: Bổ sung các cột thiếu vào bảng cũ để chống văng lỗi OperationalError
    cur.execute("PRAGMA table_info(student_competencies)")
    comp_cols = [c[1] for c in cur.fetchall()]
    if "last_misconception" not in comp_cols and len(comp_cols) > 0:
        cur.execute("ALTER TABLE student_competencies ADD COLUMN last_misconception TEXT DEFAULT 'Chưa có'")

    cur.execute("PRAGMA table_info(submissions)")
    sub_cols = [c[1] for c in cur.fetchall()]
    if "misconception" not in sub_cols and len(sub_cols) > 0:
        cur.execute("ALTER TABLE submissions ADD COLUMN misconception TEXT DEFAULT ''")
    if "attempt_count" not in sub_cols and len(sub_cols) > 0:
        cur.execute("ALTER TABLE submissions ADD COLUMN attempt_count INTEGER DEFAULT 1")

    # 4. Tài khoản Giáo viên mặc định
    cur.execute("SELECT id FROM users WHERE email = 'luyennmhcmue@gmail.com'")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (account_id, email, password, full_name, role, class_name)
            VALUES ('gv_luyen', 'luyennmhcmue@gmail.com', '123456', 'Nguyễn Mỹ Luyến', 'teacher', 'Tổ Tin Học')
        """)

    # 5. Khởi tạo danh sách 400 học sinh (10 lớp x 40 học sinh) hoàn toàn sạch dữ liệu giả
    cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    if cur.fetchone()[0] < 400:
        ho_list = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng"]
        dem_list = ["Văn", "Thị", "Minh", "Đức", "Anh", "Hoàng", "Ngọc", "Thanh", "Tuấn", "Hải"]
        ten_list = ["An", "Bình", "Cường", "Dũng", "Đạt", "Hải", "Huy", "Khoa", "Kiệt", "Lâm", "Minh", "Nam", "Nghĩa", "Phúc", "Quân"]

        students_to_insert = []
        random.seed(42)
        for c_idx in range(1, 11):
            c_name = f"10A{c_idx}"
            c_prefix = f"10a{c_idx}"
            for s_num in range(1, 41):
                acc_id = f"{c_prefix}_{s_num:02d}"
                name = "Trần Minh Đức" if acc_id == "10a1_01" else f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
                email = f"{acc_id}@school.edu.vn"
                students_to_insert.append((acc_id, email, "123456", name, "student", c_name, 0, 0, "Bình thường"))

        cur.execute("DELETE FROM users WHERE role = 'student'")
        cur.executemany("""
            INSERT INTO users (account_id, email, password, full_name, role, class_name, strikes, is_locked, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, students_to_insert)

    conn.commit()
    conn.close()

# --- TÍNH TOÁN NĂNG LỰC THỰC TẾ 100% (KHÔNG SỐ LIỆU ẢO) ---
def sync_real_student_competency(account_id):
    """
    Tính toán chính xác năng lực người học dựa trên lịch sử nộp bài thực tế trong bảng submissions:
    Mastery % = (Tổng điểm cao nhất các bài đạt được trong chủ đề / Tổng điểm tối đa của chủ đề) * 100
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Lấy điểm cao nhất của từng bài mà học sinh này đã thực sự nộp
    cur.execute("""
        SELECT exercise_id, MAX(score) as best_score, COUNT(id) as attempts
        FROM submissions
        WHERE account_id = ?
        GROUP BY exercise_id
    """, (str(account_id),))
    sub_rows = cur.fetchall()
    
    # Lấy lỗi nhận thức gần nhất theo từng chủ đề
    cur.execute("""
        SELECT exercise_id, misconception
        FROM submissions
        WHERE account_id = ? AND misconception != ''
        ORDER BY submitted_at DESC
    """, (str(account_id),))
    misc_rows = cur.fetchall()
    latest_misc_by_topic = {}
    for r in misc_rows:
        prefix = r["exercise_id"].split("_")[0]
        if prefix not in latest_misc_by_topic:
            latest_misc_by_topic[prefix] = r["misconception"]

    # Tổng hợp theo từng nhóm năng lực
    best_scores = {r["exercise_id"]: r["best_score"] for r in sub_rows}
    attempts_per_ex = {r["exercise_id"]: r["attempts"] for r in sub_rows}

    for prefix, cfg in TOPIC_CONFIG.items():
        total_ex = cfg["total_ex"]
        # Lấy các bài thuộc chủ đề này
        topic_scores = [best_scores.get(f"{prefix}_{i:02d}", 0.0) for i in range(1, total_ex + 1)]
        passed_count = sum(1 for s in topic_scores if s >= 8.0)
        total_attempts = sum(attempts_per_ex.get(f"{prefix}_{i:02d}", 0) for i in range(1, total_ex + 1))
        
        # Phần trăm thành thạo thực tế = Điểm đạt được / Điểm tối đa
        total_points = sum(topic_scores)
        max_possible_points = total_ex * 10.0
        real_mastery = round((total_points / max_possible_points) * 100.0, 1)
        
        last_misc = latest_misc_by_topic.get(prefix, "Chưa ghi nhận lỗi")

        cur.execute("""
            INSERT INTO student_competencies (account_id, topic_prefix, topic_name, mastery_percent, total_attempts, passed_count, last_misconception)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(account_id, topic_prefix) DO UPDATE SET
                mastery_percent = excluded.mastery_percent,
                total_attempts = excluded.total_attempts,
                passed_count = excluded.passed_count,
                last_misconception = excluded.last_misconception
        """, (str(account_id), prefix, cfg["name"], real_mastery, total_attempts, passed_count, last_misc))

    conn.commit()
    conn.close()

def get_student_competencies(account_id):
    # Đồng bộ số liệu thực tế trước khi hiển thị
    sync_real_student_competency(account_id)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT topic_prefix, topic_name, mastery_percent, total_attempts, passed_count, last_misconception
        FROM student_competencies
        WHERE account_id = ?
        ORDER BY topic_prefix ASC
    """, (str(account_id),))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- LỘ TRÌNH THÍCH ỨNG DỰA TRÊN TIẾN TRÌNH THẬT ---
def get_adaptive_recommendation(account_id, exercise_bank):
    comps = get_student_competencies(account_id)
    if not comps:
        return []

    # Sắp xếp theo mức độ thành thạo thực tế
    sorted_comps = sorted(comps, key=lambda x: x["mastery_percent"])
    weakest = sorted_comps[0]
    focus = sorted_comps[1] if len(sorted_comps) > 1 else weakest
    strongest = sorted_comps[-1]

    # Tìm bài tập thực tế tương ứng trong ngân hàng bài
    ex_weak = next((e for e in exercise_bank if e["id"].startswith(weakest["topic_prefix"]) and e["difficulty"] == "Nhận biết"), exercise_bank[0])
    ex_focus = next((e for e in exercise_bank if e["id"].startswith(focus["topic_prefix"]) and e["difficulty"] in ["Thông hiểu", "Vận dụng"]), exercise_bank[1])
    ex_challenge = next((e for e in exercise_bank if e["id"].startswith(strongest["topic_prefix"]) and e["difficulty"] in ["Vận dụng", "Vận dụng cao"]), exercise_bank[-1])

    return [
        {
            "type": "Củng cố nền tảng",
            "badge": "🔴 Ưu tiên khắc phục",
            "exercise": ex_weak,
            "reason": f"Chủ đề '{weakest['topic_name']}' em mới hoàn thành {weakest['mastery_percent']}%. Em cần giải quyết vững bài Nhận biết này trước."
        },
        {
            "type": "Rèn luyện trọng tâm (ZPD)",
            "badge": "🟡 Vùng phát triển gần nhất",
            "exercise": ex_focus,
            "reason": f"Chủ đề '{focus['topic_name']}' đạt {focus['mastery_percent']}%. Bài tập này phù hợp nhất với trình độ thực tế hiện tại của em."
        },
        {
            "type": "Thử thách nâng cao",
            "badge": "🟢 Thử thách bứt phá",
            "exercise": ex_challenge,
            "reason": f"Phát huy kết quả học tập ở chủ đề '{strongest['topic_name']}' ({strongest['mastery_percent']}%)."
        }
    ]

# --- GHI NHẬN NỘP BÀI VÀ XÁC THỰC ---
def save_submission(account_id, exercise_id, code, status, score=0, misconception=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM submissions WHERE account_id = ? AND exercise_id = ?", (str(account_id), str(exercise_id)))
    current_attempt = cur.fetchone()[0] + 1
    
    cur.execute("""
        INSERT INTO submissions (account_id, exercise_id, code, status, score, misconception, attempt_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(account_id), str(exercise_id), str(code), str(status), float(score), misconception, current_attempt))
    conn.commit()
    conn.close()
    
    # Đồng bộ tính toán lại ngay sau khi nộp
    sync_real_student_competency(account_id)

def get_exercise_submission_count(account_id, exercise_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM submissions WHERE account_id = ? AND exercise_id = ?", (str(account_id), str(exercise_id)))
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_student_highest_score(account_id=None, exercise_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if account_id and exercise_id:
            cur.execute("SELECT MAX(score) FROM submissions WHERE account_id = ? AND exercise_id = ?", (str(account_id), str(exercise_id)))
        elif account_id:
            cur.execute("SELECT MAX(score) FROM submissions WHERE account_id = ?", (str(account_id),))
        else:
            cur.execute("SELECT MAX(score) FROM submissions")
        res = cur.fetchone()
        conn.close()
        return res[0] if res and res[0] is not None else 0.0
    except Exception:
        return 0.0

def authenticate_user(login_id, password):
    if not login_id or not password:
        return None, "Vui lòng nhập đầy đủ tài khoản và mật khẩu."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM users 
        WHERE (email = ? OR account_id = ?) AND password = ?
    """, (str(login_id).strip(), str(login_id).strip(), str(password).strip()))
    user = cur.fetchone()
    conn.close()
    if not user:
        return None, "Tài khoản hoặc mật khẩu không chính xác."
    u_dict = dict(user)
    if u_dict.get("is_locked") == 1:
        return None, "Tài khoản đang bị tạm khóa do vi phạm kỷ luật!"
    return u_dict, "Đăng nhập thành công!"

authenticate = authenticate_user

# --- BENCHMARK THỰC TẾ 100% CHO GIÁO VIÊN ---
def get_real_benchmark_report():
    conn = get_connection()
    cur = conn.cursor()
    # Tổng hợp trực tiếp từ submissions thực tế: số bài nộp thật, điểm thật, số bài hoàn thành
    cur.execute("""
        SELECT 
            u.account_id,
            u.full_name,
            u.class_name,
            u.status,
            u.strikes,
            u.is_locked,
            COUNT(s.id) as total_submissions,
            COALESCE(MAX(s.score), 0.0) as highest_score,
            COALESCE(ROUND(AVG(s.score), 1), 0.0) as avg_score,
            COUNT(DISTINCT CASE WHEN s.score >= 8.0 THEN s.exercise_id END) as passed_exercises
        FROM users u
        LEFT JOIN submissions s ON u.account_id = s.account_id
        WHERE u.role = 'student'
        GROUP BY u.account_id
        ORDER BY u.class_name ASC, u.account_id ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_students():
    return get_real_benchmark_report()

def get_locked_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, account_id, full_name, class_name, strikes, is_locked FROM users WHERE is_locked = 1")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def unlock_user(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_locked = 0, strikes = 0, status = 'Bình thường' WHERE account_id = ?", (str(account_id),))
    conn.commit()
    conn.close()

def add_strike(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT strikes FROM users WHERE account_id = ?", (str(account_id),))
    row = cur.fetchone()
    if row:
        new_strikes = row['strikes'] + 1
        is_locked = 1 if new_strikes >= 3 else 0
        status = 'Tạm khóa' if is_locked else 'Cảnh báo'
        cur.execute("UPDATE users SET strikes = ?, is_locked = ?, status = ? WHERE account_id = ?", (new_strikes, is_locked, status, str(account_id)))
        conn.commit()
    conn.close()

def change_user_password(identifier, old_password, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE (email = ? OR account_id = ?) AND password = ?", (str(identifier).strip(), str(identifier).strip(), str(old_password).strip()))
    user = cur.fetchone()
    if not user:
        conn.close()
        return False
    cur.execute("UPDATE users SET password = ? WHERE id = ?", (str(new_password).strip(), user['id']))
    conn.commit()
    conn.close()
    return True