import os
import random
import sqlite3
import sqlite3
import datetime

def init_telemetry_table(db_path: str = "data/database"):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS thesis_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                timestamp TEXT,
                concept_id TEXT,
                bkt_prior REAL,
                bkt_posterior REAL,
                scaffold_level INTEGER,
                is_correct INTEGER,
                ast_valid INTEGER
            )
        """)

def log_learning_step(db_path: str, student_id: str, concept: str, prior: float, post: float, level: int, is_correct: bool, ast_valid: bool):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            INSERT INTO thesis_telemetry 
            (student_id, timestamp, concept_id, bkt_prior, bkt_posterior, scaffold_level, is_correct, ast_valid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, datetime.datetime.now().isoformat(), concept, prior, post, level, int(is_correct), int(ast_valid)))
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "database.db")

COMPETENCY_TOPICS = [
    {"prefix": "C1", "name": "Vào/Ra & Biến cơ sở (Bài 16-18)", "total_ex": 40},
    {"prefix": "C2", "name": "Rẽ nhánh & Vòng lặp (Bài 19-21)", "total_ex": 40},
    {"prefix": "C3", "name": "Xâu ký tự & Kiểu List (Bài 22-25)", "total_ex": 40},
    {"prefix": "C4", "name": "Hàm & Chương trình con (Bài 26-28)", "total_ex": 40},
    {"prefix": "C5", "name": "Thuật toán & Gỡ lỗi (Bài 29-30)", "total_ex": 40}
]

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Bảng tài khoản người dùng
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
            is_activated INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Chưa kích hoạt'
        )
    """)
    
    # 2. Bảng bài nộp thật
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

    # 3. Bảng Ma trận năng lực
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

    # Migration bổ sung cột nếu bảng cũ thiếu
    cur.execute("PRAGMA table_info(users)")
    user_cols = [c[1] for c in cur.fetchall()]
    if "is_activated" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN is_activated INTEGER DEFAULT 0")

    cur.execute("PRAGMA table_info(submissions)")
    sub_cols = [c[1] for c in cur.fetchall()]
    if "misconception" not in sub_cols:
        cur.execute("ALTER TABLE submissions ADD COLUMN misconception TEXT DEFAULT ''")
    if "attempt_count" not in sub_cols:
        cur.execute("ALTER TABLE submissions ADD COLUMN attempt_count INTEGER DEFAULT 1")

    cur.execute("PRAGMA table_info(student_competencies)")
    comp_cols = [c[1] for c in cur.fetchall()]
    if "last_misconception" not in comp_cols:
        cur.execute("ALTER TABLE student_competencies ADD COLUMN last_misconception TEXT DEFAULT 'Chưa có'")

    # 4. Tài khoản Giáo viên quản trị mặc định
    cur.execute("SELECT id FROM users WHERE email = 'luyennmhcmue@gmail.com'")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (account_id, email, password, full_name, role, class_name, is_activated, status)
            VALUES ('gv_luyen', 'luyennmhcmue@gmail.com', '123456', 'Nguyễn Mỹ Luyến', 'teacher', 'Tổ Tin Học', 1, 'Bình thường')
        """)

    # 5. Khởi tạo danh sách 400 học sinh: 100% SẠCH SẼ, KHÔNG GHI KHỐNG KỶ LUẬT
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
                # Mọi học sinh ban đầu đều bình đẳng: 0 lỗi, chưa khóa, chưa kích hoạt
                students_to_insert.append((acc_id, email, "123456", name, "student", c_name, 0, 0, 0, "Chưa kích hoạt"))

        cur.execute("DELETE FROM users WHERE role = 'student'")
        cur.executemany("""
            INSERT INTO users (account_id, email, password, full_name, role, class_name, strikes, is_locked, is_activated, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, students_to_insert)

    # 6. DỌN SẠCH CÁC TRẠNG THÁI GÁN KHỐNG TỪ TRƯỚC TRONG CSDL CŨ
    # Mở khóa và xóa sạch strikes cho những học sinh bị gán ảo trước đó
    cur.execute("""
        UPDATE users 
        SET is_locked = 0, strikes = 0 
        WHERE account_id IN ('10a2_15', '10a5_22', '10a7_09', '10a9_31')
    """)

    # Đồng bộ trạng thái: Ai chưa kích hoạt thì giữ 'Chưa kích hoạt'
    cur.execute("""
        UPDATE users 
        SET status = CASE 
            WHEN is_locked = 1 THEN 'Tạm khóa'
            WHEN is_activated = 1 THEN 'Bình thường'
            ELSE 'Chưa kích hoạt'
        END
        WHERE role = 'student'
    """)

    conn.commit()
    conn.close()

# --- XÁC THỰC VÀ KÍCH HOẠT HỌC SINH KHI THỰC SỰ ĐĂNG NHẬP ---
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

    if not user:
        conn.close()
        return None, "Tài khoản hoặc mật khẩu không chính xác."
    
    u_dict = dict(user)
    if u_dict.get("is_locked") == 1:
        conn.close()
        return None, "Tài khoản đang bị tạm khóa do vi phạm kỷ luật!"

    # Kích hoạt tài khoản khi học sinh thực sự đăng nhập vào hệ thống
    if u_dict.get("is_activated") == 0:
        cur.execute("UPDATE users SET is_activated = 1, status = 'Bình thường' WHERE id = ?", (u_dict["id"],))
        conn.commit()
        u_dict["is_activated"] = 1
        u_dict["status"] = "Bình thường"

    conn.close()
    return u_dict, "Đăng nhập thành công!"

authenticate = authenticate_user

# --- TÍNH TOÁN MA TRẬN NĂNG LỰC THỰC TẾ 100% ---
def sync_real_student_competency(account_id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT exercise_id, MAX(score) as best_score, COUNT(id) as attempts
        FROM submissions
        WHERE account_id = ?
        GROUP BY exercise_id
    """, (str(account_id),))
    sub_rows = cur.fetchall()
    
    cur.execute("""
        SELECT exercise_id, misconception
        FROM submissions
        WHERE account_id = ? AND misconception != ''
        ORDER BY submitted_at DESC
    """, (str(account_id),))
    misc_rows = cur.fetchall()
    latest_misc = {}
    for r in misc_rows:
        p = r["exercise_id"].split("_")[0]
        if p not in latest_misc:
            latest_misc[p] = r["misconception"]

    best_scores = {r["exercise_id"]: r["best_score"] for r in sub_rows}
    attempts_map = {r["exercise_id"]: r["attempts"] for r in sub_rows}

    for t in COMPETENCY_TOPICS:
        p = t["prefix"]
        total_ex = t["total_ex"]
        
        topic_scores = [best_scores.get(f"{p}_{i:02d}", 0.0) for i in range(1, total_ex + 1)]
        passed_cnt = sum(1 for s in topic_scores if s >= 8.0)
        total_att = sum(attempts_map.get(f"{p}_{i:02d}", 0) for i in range(1, total_ex + 1))
        
        pts = sum(topic_scores)
        mastery = round((pts / (total_ex * 10.0)) * 100.0, 1)
        misc = latest_misc.get(p, "Chưa ghi nhận lỗi")

        cur.execute("""
            INSERT INTO student_competencies (account_id, topic_prefix, topic_name, mastery_percent, total_attempts, passed_count, last_misconception)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(account_id, topic_prefix) DO UPDATE SET
                mastery_percent = excluded.mastery_percent,
                total_attempts = excluded.total_attempts,
                passed_count = excluded.passed_count,
                last_misconception = excluded.last_misconception
        """, (str(account_id), p, t["name"], mastery, total_att, passed_cnt, misc))

    conn.commit()
    conn.close()

def get_student_competencies(account_id):
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

# --- LỘ TRÌNH THÍCH ỨNG DỰA TRÊN DỮ LIỆU THẬT ---
def get_adaptive_recommendation(account_id, exercise_bank):
    comps = get_student_competencies(account_id)
    if not comps:
        return []

    sorted_comps = sorted(comps, key=lambda x: x["mastery_percent"])
    weakest = sorted_comps[0]
    focus = sorted_comps[1] if len(sorted_comps) > 1 else weakest
    strongest = sorted_comps[-1]

    ex_weak = next((e for e in exercise_bank if e["id"].startswith(weakest["topic_prefix"]) and e["difficulty"] == "Nhận biết"), exercise_bank[0])
    ex_focus = next((e for e in exercise_bank if e["id"].startswith(focus["topic_prefix"]) and e["difficulty"] in ["Thông hiểu", "Vận dụng"]), exercise_bank[1])
    ex_challenge = next((e for e in exercise_bank if e["id"].startswith(strongest["topic_prefix"]) and e["difficulty"] in ["Vận dụng", "Vận dụng cao"]), exercise_bank[-1])

    return [
        {
            "type": "Củng cố nền tảng",
            "badge": "🔴 Ưu tiên khắc phục",
            "exercise": ex_weak,
            "reason": f"Chủ đề '{weakest['topic_name']}' đạt {weakest['mastery_percent']}%. Em cần giải quyết bài Nhận biết này trước."
        },
        {
            "type": "Rèn luyện trọng tâm (ZPD)",
            "badge": "🟡 Vùng phát triển gần nhất",
            "exercise": ex_focus,
            "reason": f"Chủ đề '{focus['topic_name']}' đạt {focus['mastery_percent']}%. Bài tập này phù hợp nhất với năng lực hiện tại của em."
        },
        {
            "type": "Thử thách nâng cao",
            "badge": "🟢 Thử thách bứt phá",
            "exercise": ex_challenge,
            "reason": f"Phát huy năng lực ở chủ đề '{strongest['topic_name']}' ({strongest['mastery_percent']}%)."
        }
    ]

# --- BÁO CÁO BENCHMARK 100% THỰC TẾ CHO GIÁO VIÊN ---
def get_real_benchmark_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            u.account_id,
            u.full_name,
            u.class_name,
            u.is_locked,
            u.is_activated,
            CASE 
                WHEN u.is_locked = 1 THEN 'Tạm khóa'
                WHEN u.is_activated = 0 THEN 'Chưa kích hoạt'
                ELSE 'Bình thường'
            END as status_display,
            COUNT(s.id) as total_submissions,
            COUNT(DISTINCT CASE WHEN s.score >= 8.0 THEN s.exercise_id END) as passed_exercises,
            COALESCE(MAX(s.score), 0.0) as highest_score,
            COALESCE(ROUND(AVG(s.score), 1), 0.0) as avg_score
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

def save_submission(account_id, exercise_id, code, status, score=0, misconception=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM submissions WHERE account_id = ? AND exercise_id = ?", (str(account_id), str(exercise_id)))
    current_attempt = cur.fetchone()[0] + 1
    
    cur.execute("""
        INSERT INTO submissions (account_id, exercise_id, code, status, score, misconception, attempt_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(account_id), str(exercise_id), str(code), str(status), float(score), misconception, current_attempt))
    
    cur.execute("UPDATE users SET is_activated = 1, status = 'Bình thường' WHERE account_id = ? AND is_locked = 0", (str(account_id),))
    conn.commit()
    conn.close()
    
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
    cur.execute("UPDATE users SET is_locked = 0, strikes = 0, status = CASE WHEN is_activated = 1 THEN 'Bình thường' ELSE 'Chưa kích hoạt' END WHERE account_id = ?", (str(account_id),))
    conn.commit()
    conn.close()

def add_strike(account_id):
    """Chỉ tăng strikes khi học sinh thực sự vi phạm trong giờ học"""
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

def reset_all_data_to_clean():
    """Hàm dành cho Giáo viên: Đặt lại toàn bộ dữ liệu kiểm thử về 0 sạch sẽ"""
    conn = get_connection()
    cur = conn.cursor()
    # Xóa sạch toàn bộ bài nộp
    cur.execute("DELETE FROM submissions")
    # Đặt lại ma trận năng lực về 0
    cur.execute("DELETE FROM student_competencies")
    # Đặt lại trạng thái 400 học sinh về ban đầu (chưa kích hoạt, 0 lỗi, không khóa)
    cur.execute("""
        UPDATE users 
        SET strikes = 0, is_locked = 0, is_activated = 0, status = 'Chưa kích hoạt' 
        WHERE role = 'student'
    """)
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