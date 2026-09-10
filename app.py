from pathlib import Path
import streamlit as st
import pandas as pd
import json

from src.db import (
    init_db,
    get_connection,
    authenticate_user,
    get_student_highest_score,
    save_submission,
    change_user_password,
    unlock_user_account,
    generate_forgot_otp,
    reset_password_with_otp
)
from src.curriculum import CHAPTER_NAMES, SGK_CURRICULUM, CURRICULUM_EXERCISES
from src.judge import grade_code
from src.ai_agent import get_gemini_socratic_response

# Khởi tạo cơ sở dữ liệu
init_db()

st.set_page_config(
    page_title="EduCoder 10 - Lập trình Tin học 10",
    page_icon="💻",
    layout="wide"
)

# Tùy chỉnh CSS giao diện hiện đại, chống tràn chữ
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #006699 0%, #0099cc 100%);
        padding: 14px 22px;
        border-radius: 8px;
        color: white;
        margin-bottom: 18px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .custom-card { 
        background-color: rgba(128, 128, 128, 0.08) !important; 
        border: 1px solid rgba(128, 128, 128, 0.25) !important; 
        border-radius: 8px; 
        padding: 18px 22px; 
        margin-bottom: 14px; 
        box-sizing: border-box !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    .card-title {
        font-size: 17px;
        font-weight: bold;
        color: #0074A6;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái phiên làm việc (Session State)
if "user" not in st.session_state:
    st.session_state.user = None
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏠 Trang chủ"
if "active_exercise" not in st.session_state:
    st.session_state.active_exercise = CURRICULUM_EXERCISES["c1"][0]
if "active_ch" not in st.session_state:
    st.session_state.active_ch = "c1"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_verdict" not in st.session_state:
    st.session_state.last_verdict = None

# ==============================================================================
# KHU VỰC CHƯA ĐĂNG NHẬP (ĐĂNG NHẬP & QUÊN MẬT KHẨU)
# ==============================================================================
if not st.session_state.user:
    st.markdown('<div class="main-header">💻 EDUCODER 10 - HỆ THỐNG LUYỆN LẬP TRÌNH TIN HỌC 10 (GDPT 2018)</div>', unsafe_allow_html=True)
    tab_login, tab_forgot = st.tabs(["Đăng Nhập", "Quên Mật Khẩu"])

    with tab_login:
        col_l1, col_l2 = st.columns([1.2, 1])
        with col_l1:
            u_acc = st.text_input("Tài khoản (mã học sinh ví dụ: 10a1_01 hoặc Gmail):", key="login_acc")
            u_pwd = st.text_input("Mật khẩu:", type="password", key="login_pwd")
            if st.button("Đăng Nhập", type="primary", use_container_width=True):
                if not u_acc or not u_pwd:
                    st.warning("Vui lòng điền đầy đủ tài khoản và mật khẩu.")
                else:
                    user_data, msg = authenticate_user(u_acc, u_pwd)
                    if user_data:
                        st.session_state.user = user_data
                        st.session_state.nav_page = "🏠 Trang chủ"
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        with col_l2:
            st.info("""
            **Quy ước tài khoản học sinh:**
            - **Mã học sinh:** Từ lớp 10A1 đến 10A10 (ví dụ: `10a1_01`, `10a5_10`, `10a10_45`).
            - **Mật khẩu mặc định ban đầu:** `123456`
            - Giáo viên đăng nhập trực tiếp bằng Gmail cá nhân.
            """)

    with tab_forgot:
        st.markdown("##### Khôi phục mật khẩu tài khoản")
        f_step = st.radio("Chọn thao tác:", ["1. Yêu cầu gửi mã OTP", "2. Đặt lại mật khẩu bằng OTP"], horizontal=True)
        if "1." in f_step:
            f_target = st.text_input("Nhập tài khoản hoặc Email đã đăng ký:", key="fg_acc")
            if st.button("Gửi mã OTP xác nhận", type="primary"):
                if not f_target:
                    st.warning("Vui lòng nhập tài khoản hoặc email.")
                else:
                    otp, dest, send_msg = generate_forgot_otp(f_target)
                    if otp:
                        st.success(f"✅ {send_msg}")
                    else:
                        st.error(send_msg)
        else:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                r_target = st.text_input("Tài khoản hoặc Email:", key="rst_acc")
                r_otp = st.text_input("Mã OTP 6 số:", key="rst_otp")
            with col_r2:
                r_new_pw = st.text_input("Mật khẩu mới:", type="password", key="rst_npw")
                r_cf_pw = st.text_input("Xác nhận mật khẩu mới:", type="password", key="rst_cpw")
            if st.button("Xác nhận đổi mật khẩu", type="primary"):
                if r_new_pw != r_cf_pw:
                    st.error("Mật khẩu xác nhận không khớp.")
                elif len(r_new_pw) < 6:
                    st.warning("Mật khẩu mới phải có ít nhất 6 ký tự.")
                else:
                    ok, msg = reset_password_with_otp(r_target, r_otp, r_new_pw)
                    if ok:
                        st.success(msg)
                        st.info("Vui lòng quay lại tab 'Đăng Nhập' để tiếp tục.")
                    else:
                        st.error(msg)
    st.stop()

# ==============================================================================
# KHU VỰC ĐÃ ĐĂNG NHẬP (PHÂN QUYỀN RBAC)
# ==============================================================================
user = st.session_state.user
is_teacher = (user["role"] == "teacher")

# Định danh vai trò trên thanh Navbar
if user:
    if is_teacher:
        clean_name = user['full_name'].replace("Thầy/Cô", "").replace("Cô", "").replace("Thầy", "").strip()
        user_tag = f"👨‍🏫 Thầy/Cô {clean_name}" if clean_name else "👨‍🏫 Thầy/Cô Giáo viên"
    else:
        user_tag = f"👤 {user['full_name']} ({user['class_name']})"

# Danh sách trang điều hướng
nav_options = ["🏠 Trang chủ", "📖 Lý thuyết SGK", "📝 Kho Bài Tập Python", "💬 Trợ lý học tập AI"]
if is_teacher:
    nav_options.append("📊 Báo cáo Benchmark")
nav_options.append(user_tag)

# Đồng bộ nếu tab hiện tại không có trong danh sách
if st.session_state.nav_page not in nav_options:
    st.session_state.nav_page = "🏠 Trang chủ"

st.markdown('<div class="main-header">💻 EDUCODER 10 - HỆ THỐNG LUYỆN LẬP TRÌNH VÀ TRỢ LÝ TIN HỌC 10 (GDPT 2018)</div>', unsafe_allow_html=True)

selected_nav = st.radio(
    "Điều hướng:",
    options=nav_options,
    index=nav_options.index(st.session_state.nav_page),
    horizontal=True,
    label_visibility="collapsed"
)
if selected_nav != st.session_state.nav_page:
    st.session_state.nav_page = selected_nav
    st.rerun()

# ----------------- 1. TRANG CHỦ -----------------
if st.session_state.nav_page == "🏠 Trang chủ":
    col_h1, col_h2 = st.columns([2.2, 1])
    with col_h1:
        if is_teacher:
            clean_teacher_name = user['full_name'].replace("Thầy/Cô", "").replace("Cô", "").replace("Thầy", "").strip()
            display_teacher_name = clean_teacher_name if clean_teacher_name else "Giáo viên"

            st.markdown(f"### Kính chào Thầy/Cô {display_teacher_name}!")
            st.markdown("**Đơn vị:** Tổ Tin Học | **Vai trò:** Quản trị & Giảng dạy Bộ môn")
            st.success("👨‍🏫 **Trạng thái:** Hệ thống phân quyền Giáo viên sẵn sàng. Thầy/Cô có thể vào duyệt Kho bài tập, chạy thử bộ Testcases hoặc theo dõi tiến độ lớp học qua Báo cáo Benchmark.")
        else:
            st.markdown(f"### Chào mừng bạn {user['full_name']}!")
            st.markdown(f"**Lớp:** {user['class_name']} | **Vai trò:** Học sinh")
            st.info("💻 **Trạng thái:** Tài khoản hoạt động bình thường. Em hãy chọn bài tập để bắt đầu rèn luyện lập trình nhé!")

        st.write("")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📖 Đọc Lý thuyết SGK", use_container_width=True):
                st.session_state.nav_page = "📖 Lý thuyết SGK"
                st.rerun()
        with btn_col2:
            if st.button("📝 Vào Kho Bài Tập Python", use_container_width=True):
                st.session_state.nav_page = "📝 Kho Bài Tập Python"
                st.rerun()

    with col_h2:
        with st.container(border=True):
            st.markdown("#### 📌 THÔNG TIN HỌC VỤ KHỐI 10")
            st.markdown("""
            - **Chương trình:** SGK Tin học 10 (Chủ đề 5 - Lập trình Python).
            - **Quy chế chấm điểm:** Điểm được lưu tự động trên thang 10.
            - **Liêm chính học thuật:** Trợ lý Socratic chỉ gợi mở phương pháp, không cho full code giải sẵn.
            """)

# ----------------- 2. LÝ THUYẾT SGK TIN HỌC 10 -----------------
elif st.session_state.nav_page == "📖 Lý thuyết SGK":
    st.markdown("### CỐT LÕI KIẾN THỨC SGK TIN HỌC 10")
    lesson_keys = list(SGK_CURRICULUM.keys())
    selected_lesson_key = st.selectbox(
        "Chọn bài học:",
        options=lesson_keys,
        format_func=lambda k: SGK_CURRICULUM[k]["name"]
    )
    lesson_data = SGK_CURRICULUM[selected_lesson_key]
    st.write("")
    with st.container(border=True):
        st.markdown(f'<div class="card-title">📘 {lesson_data["name"]}</div>', unsafe_allow_html=True)
        st.markdown(lesson_data["content"])

# ----------------- 3. KHO BÀI TẬP PYTHON -----------------
elif st.session_state.nav_page == "📝 Kho Bài Tập Python":
    st.markdown("### KHO BÀI TẬP PYTHON")
    col_k1, col_k2 = st.columns([1.2, 2.5])

    ch_keys = list(CURRICULUM_EXERCISES.keys())
    with col_k1:
        chosen_ch = st.selectbox(
            "Chọn chương kiến thức:",
            options=ch_keys,
            format_func=lambda x: CHAPTER_NAMES.get(x, f"Chương {x.replace('c','')}")
        )
        exercises = CURRICULUM_EXERCISES.get(chosen_ch, [])
        lvl = st.radio("Mức độ nhận thức:", ["Tất cả", "Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"], horizontal=True)
        filtered_ex = [e for e in exercises if lvl == "Tất cả" or e.get("level") == lvl]

    with col_k2:
        if not filtered_ex:
            st.warning("⚠️ Hiện chưa có bài tập nào ở mức độ này trong chương đã chọn.")
        else:
            with col_k1:
                selected_ex = st.selectbox(
                    "Chọn bài thực hành:",
                    options=filtered_ex,
                    format_func=lambda x: f"[{x['code']}] {x['title']}"
                )

            if selected_ex:
                u_target = user.get("account_id") or user.get("email")
                high_sc = get_student_highest_score(u_target, selected_ex["code"]) if not is_teacher else 10.0
                score_badge = "<b>Chế độ:</b> Giáo viên xem trước & kiểm thử" if is_teacher else f"<b>Điểm cao nhất của bạn:</b> {high_sc}/10"

                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">📄 {selected_ex['title']} ({selected_ex['level']})</div>
                    <b>Mã bài:</b> <code>{selected_ex['code']}</code> | {score_badge}<br><br>
                    <b>Yêu cầu đề bài:</b><br>{selected_ex['problem']}<br><br>
                    <b>Gợi ý:</b><br>{selected_ex['hint']}
                </div>
                """, unsafe_allow_html=True)

                btn_label = "🚀 Chạy thử bài tập với Trợ lý AI" if is_teacher else "🚀 Bắt đầu làm bài với Trợ lý AI"
                if st.button(btn_label, type="primary"):
                    st.session_state.active_exercise = selected_ex
                    st.session_state.active_ch = chosen_ch
                    st.session_state.nav_page = "💬 Trợ lý học tập AI"
                    st.rerun()

# ----------------- 4. KHÔNG GIAN LÀM BÀI & TRỢ LÝ AI -----------------
elif st.session_state.nav_page == "💬 Trợ lý học tập AI":
    active_ex = st.session_state.active_exercise
    if not active_ex:
        st.session_state.active_exercise = CURRICULUM_EXERCISES["c1"][0]
        active_ex = st.session_state.active_exercise

    # KIỂM TRA TRẠNG THÁI KHÓA TÀI KHOẢN DO VI PHẠM KỶ LUẬT
    if user.get("is_locked") == 1:
        st.error("🚫 **TÀI KHOẢN CỦA EM ĐÃ BỊ KHÓA DO VI PHẠM KỶ LUẬT PHÁT NGÔN 3 LẦN!**")
        st.warning("Toàn bộ quyền làm bài, nộp bài và sử dụng Trợ lý AI đã bị đình chỉ. Em hãy liên hệ Thầy/Cô bộ môn Tin học để được xem xét mở lại tài khoản.")
        st.stop()

    st.markdown(f"### 💻 LÀM BÀI: [{active_ex['code']}] {active_ex['title']}")
    if is_teacher:
        st.caption("💡 Chế độ Giáo viên: Thầy/Cô có thể chạy thử mã nguồn hoặc trải nghiệm tư vấn Socratic của Trợ lý AI.")
    else:
        st.caption("💡 Hãy tự suy nghĩ thuật toán. Trợ lý Socratic sẽ hướng dẫn tư duy từng bước mà không giải hộ.")

    col_work, col_chat = st.columns([1.3, 1.2])

    with col_work:
        st.markdown(f"""
        <div class="custom-card">
            <div class="card-title">🎯 ĐỀ BÀI: {active_ex['title']} ({active_ex['level']})</div>
            {active_ex['problem']}<br><br>
            <b>💡 Gợi ý:</b> {active_ex['hint']}
        </div>
        """, unsafe_allow_html=True)

        student_code = st.text_area(
            "Trình soạn thảo mã nguồn Python:",
            height=260,
            value=f"# Viết mã nguồn cho bài {active_ex['code']}\n",
            key=f"editor_{active_ex['code']}"
        )

        if st.button("🚀 Nộp bài & Chấm điểm", type="primary", use_container_width=True):
            with st.spinner("Hệ thống sandbox đang chạy qua các Testcases..."):
                judge_res = grade_code(student_code, active_ex.get("testcases_json", "[]"))
                st.session_state.last_verdict = judge_res

            # Lưu vào cơ sở dữ liệu nếu là học sinh
            u_target = user.get("account_id") or user.get("email")
            save_submission(
                account_id=u_target,
                exercise_id=active_ex["code"],
                score=judge_res["score"],
                status=judge_res["status"],
                code=student_code
            )

            if judge_res["verdict"] == "AC":
                st.success(f"🎉 ACCEPTED (AC): {judge_res['score']}/10 Điểm!")
            else:
                st.error(f"❌ {judge_res['status']}: {judge_res['score']}/10 Điểm")
                st.code(judge_res["details"])
                if judge_res["failed_line"]:
                    st.warning(f"⚠️ Phát hiện dòng lệnh nghi vấn gây lỗi: Dòng số {judge_res['failed_line']}")

                # Tự động tạo phân tích Socratic khi làm sai
                ctx = {
                    "title": active_ex["title"],
                    "problem": active_ex["problem"],
                    "student_code": student_code,
                    "verdict": judge_res["verdict"],
                    "judge_details": judge_res["details"],
                    "failed_line": judge_res["failed_line"]
                }
                ai_advice = get_gemini_socratic_response("Hãy giúp phân tích lỗi sai và đặt câu hỏi gợi mở Socratic.", ctx)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_advice})

    with col_chat:
        with st.container(border=True):
            chat_head_c1, chat_head_c2 = st.columns([2, 1])
            with chat_head_c1:
                st.markdown("#### 🤖 Trợ lý Socratic AI")
            with chat_head_c2:
                if st.button("🗑️ Xóa chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()

            chat_container = st.container(height=350)
            for msg in st.session_state.chat_history:
                with chat_container.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_q = st.chat_input("Hỏi AI phương pháp giải hoặc nguyên lý...")
            if user_q:
                st.session_state.chat_history.append({"role": "user", "content": user_q})
                ctx = {
                    "title": active_ex["title"],
                    "problem": active_ex["problem"],
                    "student_code": student_code,
                    "verdict": st.session_state.last_verdict.get("verdict", "N/A") if st.session_state.last_verdict else "N/A",
                    "judge_details": st.session_state.last_verdict.get("details", "") if st.session_state.last_verdict else "",
                    "failed_line": st.session_state.last_verdict.get("failed_line", None) if st.session_state.last_verdict else None
                }
                ai_reply = get_gemini_socratic_response(user_q, ctx)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.rerun()

# ----------------- 5. BÁO CÁO BENCHMARK (DÀNH CHO GIÁO VIÊN) -----------------
elif st.session_state.nav_page == "📊 Báo cáo Benchmark" and is_teacher:
    st.markdown("### 📊 BÁO CÁO BENCHMARK & THEO DÕI HỌC TẬP")
    conn = get_connection()
    df_users = pd.read_sql_query("SELECT account_id, full_name, class_name, status, is_locked FROM users WHERE role = 'student'", conn)
    df_subs = pd.read_sql_query("SELECT account_id, exercise_id, score, status, created_at FROM submissions", conn)
    conn.close()

    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng số học sinh quản lý", len(df_users))
    m2.metric("Tổng lượt chấm tự động", len(df_subs))
    ac_subs = len(df_subs[df_subs["status"].str.contains("Accepted|AC", case=False, na=False)]) if not df_subs.empty else 0
    m3.metric("Tỷ lệ bài làm đạt AC", f"{(ac_subs / len(df_subs) * 100):.1f}%" if len(df_subs) > 0 else "0%")

    st.write("")
    st.markdown("##### 📋 Danh sách học sinh theo khối")
    st.dataframe(df_users, use_container_width=True)
    # Đặt đoạn này vào khu vực giao diện dành riêng cho Giáo viên (is_teacher == True)
st.markdown("---")
st.markdown("### 🛡️ Quản lý Kỷ luật & Mở khóa Tài khoản Học sinh")

# Import hàm từ db nếu chưa có
from src.db import get_locked_users, unlock_user

locked_students = get_locked_users()
if locked_students:
    st.warning(f"⚠️ Hiện có {len(locked_students)} học sinh đang bị khóa tài khoản do vi phạm kỷ luật.")
    for s in locked_students:
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
           st.write(f"👤 **{s['full_name']}** (Mã: `{s['account_id']}` - Lớp: {dict(s).get('class_name', 'N/A')})")
        with c2:
            st.error(f"Số lỗi: {s['strikes']}/3 lần")
        with c3:
            if st.button(f"🔓 Mở khóa", key=f"unlock_btn_{s['id']}"):
                unlock_user(s['account_id'])
                st.success(f"Đã mở khóa thành công cho tài khoản {s['account_id']}!")
                st.rerun()
else:
    st.info("👍 Hệ thống an toàn: Không có học sinh nào đang bị khóa tài khoản.")
# ----------------- 6. HỒ SƠ CÁ NHÂN & ĐỔI MẬT KHẨU -----------------
# 🛡️ Quản lý Kỷ luật & Mở khóa Tài khoản Học sinh (Đã căn chuẩn thụt lề 4 khoảng trắng)
    st.markdown("---")
    st.markdown("### 🛡️ Quản lý Kỷ luật & Mở khóa Tài khoản Học sinh")
    
    from src.db import get_locked_users, unlock_user
    
    locked_students = get_locked_users()
    if locked_students:
        st.warning(f"⚠️ Hiện có {len(locked_students)} học sinh đang bị khóa tài khoản do vi phạm kỷ luật.")
        for s in locked_students:
            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                st.write(f"👤 **{s['full_name']}** (Mã: `{s['account_id']}` - Lớp: {s.get('class_name', 'N/A')})")
            with c2:
                st.error(f"Số lỗi: {s['strikes']}/3 lần")
            with c3:
                if st.button(f"🔓 Mở khóa", key=f"unlock_btn_{s['id']}"):
                    unlock_user(s['account_id'])
                    st.success(f"Đã mở khóa thành công cho tài khoản {s['account_id']}!")
                    st.rerun()
    else:
        st.info("👍 Hệ thống an toàn: Không có học sinh nào đang bị khóa tài khoản.")