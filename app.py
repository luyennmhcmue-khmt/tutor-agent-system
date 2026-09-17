import io
import sys
import re
import streamlit as st
import pandas as pd
from src.exercises import REAL_EXERCISES
from src.db import (
    init_db,
    authenticate_user,
    change_user_password,
    get_locked_users,
    unlock_user,
    add_strike,
    save_submission,
    get_student_highest_score,
    get_student_competencies,
    get_adaptive_recommendation,
    get_exercise_submission_count,
    get_real_benchmark_report
)

st.set_page_config(
    page_title="EduCoder 10 - Trợ lý Học Lập trình Cá nhân hóa Tin học 10",
    page_icon="💻",
    layout="wide"
)

if "db_ready" not in st.session_state:
    init_db()
    st.session_state.db_ready = True

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏠 Trang chủ"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_ex_id" not in st.session_state:
    st.session_state.current_ex_id = "C1_01"
if "doing_exercise" not in st.session_state:
    st.session_state.doing_exercise = False

# ==================== DỮ LIỆU LÝ THUYẾT 30 BÀI SGK TIN HỌC 10 ====================
LESSONS_DATA = {
    "Bài 1: Thông tin và xử lý thông tin": "### 1. Thông tin và dữ liệu\n- Dữ liệu (Data): Số liệu, văn bản, âm thanh lưu trữ trên máy tính.\n- Đơn vị đo: Bit, Byte (1B = 8 bits), KB, MB, GB, TB.\n### 2. Quá trình xử lý\n- Thu nhận -> Lưu trữ -> Xử lý (CPU) -> Xuất kết quả (Màn hình, máy in).",
    "Bài 2: Vai trò của thiết bị thông minh và tin học": "### 1. Thiết bị thông minh\n- Tự động kết nối và xử lý thông tin (Smartphone, Robot, Smart TV).\n### 2. Tác động của tin học\n- Thúc đẩy kinh tế số, xã hội số và chuyển đổi số quốc gia.",
    "Bài 3: Một số kiểu kiến trúc máy tính": "### 1. Kiến trúc Von Neumann\n- Gồm: CPU (ALU, CU, Thanh ghi), Bộ nhớ trong (RAM, ROM), Hệ thống Vào/Ra, Bus liên kết.",
    "Bài 4: Mạng máy tính và Internet": "### 1. Mạng máy tính & Internet\n- Mạng LAN, WAN và mạng toàn cầu Internet sử dụng giao thức TCP/IP, định danh qua địa chỉ IP.",
    "Bài 5: Dữ liệu trong máy tính và hệ số": "### 1. Hệ nhị phân (Binary)\n- Cơ số 2 gồm 0 và 1. Dùng bảng mã ASCII và Unicode (UTF-8) để mã hóa văn bản tiếng Việt.",
    "Bài 6: Dữ liệu âm thanh và hình ảnh": "### 1. Số hóa đa phương tiện\n- Điểm ảnh pixel (RGB). Âm thanh được lấy mẫu lượng tử hóa thành chuỗi bit.",
    "Bài 7: Phần mềm đồ họa Vector": "### 1. Đồ họa Vector (Inkscape)\n- Dựa trên công thức toán học, không bị vỡ nét khi phóng to co giãn kích thước.",
    "Bài 8: Định dạng văn bản và bảng biểu nâng cao": "### 1. Kỹ năng văn bản\n- Ngắt trang (Page Break), ngắt phần (Section Break), mục lục tự động, Header/Footer.",
    "Bài 9: Sử dụng bảng tính điện tử nâng cao": "### 1. Công thức bảng tính\n- Địa chỉ tương đối (A1), tuyệt đối ($A$1), hỗn hợp ($A1). Các hàm SUM, AVERAGE, IF, COUNTIF.",
    "Bài 10: Trình diễn đa phương tiện": "### 1. Thiết kế trang chiếu\n- Độ tương phản, phân cấp thông tin thị giác, hiệu ứng slide hợp lý.",
    "Bài 11: An toàn thông tin và bản quyền": "### 1. An toàn không gian mạng\n- Phòng chống virus, Ransomware, Phishing. Tôn trọng bản quyền phần mềm mã nguồn mở.",
    "Bài 12: Đạo đức, pháp luật môi trường số": "### 1. Ứng xử văn hóa số\n- Bảo vệ thông tin cá nhân, ứng xử văn minh trên mạng, tuân thủ Luật An ninh mạng.",
    "Bài 13: Cơ sở dữ liệu và hệ quản trị CSDL": "### 1. Khái niệm CSDL\n- CSDL lưu trữ dữ liệu có cấu trúc; hệ quản trị DBMS (SQLite, MySQL) xử lý truy vấn.",
    "Bài 14: Dịch vụ đám mây và IoT": "### 1. Đám mây & IoT\n- Cloud cung cấp tài nguyên trực tuyến; IoT kết nối vạn vật qua cảm biến.",
    "Bài 15: Trí tuệ nhân tạo (AI)": "### 1. Bản chất AI\n- Ngành khoa học máy tính mô phỏng quá trình tư duy, học tập và suy luận của con người.",
    "Bài 16: Ngôn ngữ lập trình bậc cao và Python": "### 1. Giới thiệu Python\n- Ngôn ngữ bậc cao, thông dịch, cú pháp rõ ràng.\n- Lệnh in ra màn hình: `print('Xin chào Python!')`",
    "Bài 17: Biến và lệnh gán": "### 1. Biến & Kiểu dữ liệu\n- Không bắt đầu bằng số, không trùng từ khóa.\n- Kiểu dữ liệu: `int`, `float`, `str`, `bool`.\n- Phép toán: `+`, `-`, `*`, `/`, `//` (chia nguyên), `%` (chia dư), `**` (lũy thừa).",
    "Bài 18: Các lệnh vào ra đơn giản": "### 1. Nhập và xuất dữ liệu\n- Nhập chuỗi: `s = input()`\n- Nhập số nguyên: `n = int(input())`\n- Nhập số thực: `x = float(input())`\n- Nhập nhiều số: `a, b = map(int, input().split())`",
    "Bài 19: Câu lệnh rẽ nhánh if": "### 1. Cú pháp rẽ nhánh\n```python\nif điều_kiện:\n    khối_lệnh_1\nelif điều_kiện_khác:\n    khối_lệnh_2\nelse:\n    khối_lệnh_mặc_định\n```\nLưu ý: Bắt buộc thụt lề 4 khoảng trắng.",
    "Bài 20: Câu lệnh lặp for": "### 1. Vòng lặp for\n```python\nfor i in range(start, stop, step):\n    khối_lệnh\n```\nHàm `range(n)` sinh dãy số từ 0 đến n-1.",
    "Bài 21: Câu lệnh lặp while": "### 1. Vòng lặp while\n```python\nwhile điều_kiện:\n    khối_lệnh\n```\n`break` để dừng lặp; `continue` để chuyển sang lần lặp kế tiếp.",
    "Bài 22: Kiểu dữ liệu danh sách (List)": "### 1. Khởi tạo danh sách\n`a = [10, 20, 30]`. Phần tử đầu: `a[0]`, phần tử cuối: `a[-1]`.",
    "Bài 23: Thao tác trên dữ liệu danh sách": "### 1. Phương thức danh sách\n- `len(a)`, `a.append(x)`, `a.insert(i, x)`, `a.remove(x)`, `a.sort()`.",
    "Bài 24: Xâu ký tự (String)": "### 1. Cấu trúc xâu\n- Xâu đặt trong cặp nháy đơn. Xâu trong Python là đối tượng bất biến.",
    "Bài 25: Thao tác trên xâu ký tự": "### 1. Phương thức xử lý xâu\n- `s.split()`, `s.strip()`, `s.upper()`, `s.lower()`, `s.replace()`.",
    "Bài 26: Hàm trong Python": "### 1. Định nghĩa hàm\n```python\ndef tên_hàm(tham_số):\n    khối_lệnh\n    return giá_trị\n```",
    "Bài 27: Tham số của hàm": "### 1. Tham số & Đối số\n- Hỗ trợ tham số mặc định: `def chao(ten='Bạn'):`",
    "Bài 28: Phạm vi của biến": "### 1. Biến cục bộ & Toàn cục\n- Biến trong hàm là cục bộ. Dùng từ khóa `global` để chỉnh sửa biến bên ngoài hàm.",
    "Bài 29: Nhận biết lỗi chương trình": "### 1. Ba loại lỗi chính\n- `SyntaxError`: Lỗi cú pháp.\n- `RuntimeError`: Lỗi thực thi (chia 0, truy xuất ngoài mảng).\n- `LogicError`: Lỗi sai thuật toán.",
    "Bài 30: Kiểm thử và gỡ lỗi chương trình": "### 1. Kiểm thử & Gỡ lỗi\n- Kiểm tra trường hợp thông thường và trường hợp biên (số 0, số âm, danh sách rỗng)."
}

# ==================== CÚ PHÁP CHUẨN TỔNG QUÁT (KHÔNG GIẢI HỘ) ====================
GENERIC_SYNTAX_TEMPLATES = {
    "Syntax_Missing_Quotes": "print('nội_dung_văn_bản')",
    "Syntax_Missing_Quotes_And_Cap": "print('nội_dung_văn_bản')",
    "Syntax_Print_Capitalized": "print('nội_dung_văn_bản')",
    "Syntax_Unclosed_Single_Quote": "print('nội_dung_văn_bản')",
    "Syntax_Unclosed_Double_Quote": 'print("nội_dung_văn_bản")',
    "Syntax_Unclosed_Paren": "print('nội_dung_văn_bản')",
    "Syntax_Missing_Colon": "if <điều_kiện>:\n    <khối_lệnh_thực_thi>",
    "Syntax_Indentation": "if <điều_kiện>:\n    <khối_lệnh_thụt_lề_4_khoảng_trắng>",
    "Misconception_Equal_Operator": "if <tên_biến> == <giá_trị_so_sánh>:\n    <khối_lệnh>",
    "Misconception_Type_Casting": "<tên_biến> = int(input())",
    "Logic_Missing_Print": "print(<giá_trị_cần_in>)",
    "Syntax_General": "# Cấu trúc chuẩn theo SGK Tin học 10"
}

# ==================== ĐỘNG CƠ CHẨN ĐOÁN SƯ PHẠM ====================
HEDGING_PATTERNS = [r"\bcó thể\b", r"\bcó lẽ\b", r"\bdường như\b", r"\bhình như\b", r"\bchắc là\b", r"\bđoán là\b"]

def purge_hedging(text: str) -> str:
    res = text
    for p in HEDGING_PATTERNS:
        res = re.sub(p, "bắt buộc", res, flags=re.IGNORECASE)
    return res.strip()

def diagnose_student_misconception(student_code, error_msg, actual_output, expected_output, exercise):
    code_str = student_code.strip()
    lines = code_str.splitlines()

    # 1. Bắt lỗi thiếu cặp dấu nháy khi gọi hàm print
    has_print_call = bool(re.search(r'\b(print|Print|PRINT)\b', code_str))
    missing_quotes = False
    if has_print_call:
        for line in lines:
            m = re.search(r'(?:print|Print|PRINT)\s*\((.*)\)', line)
            if m:
                inside = m.group(1).strip()
                if inside and ("'" not in inside and '"' not in inside):
                    missing_quotes = True
                    break

    has_cap_print = bool(re.search(r'\b(Print|PRINT)\b', code_str))

    # Trường hợp vừa viết hoa vừa thiếu dấu nháy
    if missing_quotes and has_cap_print:
        return (
            "Lệnh print viết hoa và thiếu cặp dấu nháy đơn ' '",
            "Mã nguồn vi phạm 2 quy chuẩn SGK: 1) Tên lệnh in bắt buộc viết thường là `print`. 2) Dòng chữ in ra màn hình bắt buộc đặt trong cặp dấu nháy đơn `' '`.",
            "Syntax_Missing_Quotes_And_Cap"
        )

    # Trường hợp thiếu cặp dấu nháy đơn
    if missing_quotes:
        return (
            "Thiếu cặp dấu nháy đơn ' ' bao quanh xâu kí tự",
            "Theo quy định tại Bài 16 SGK Tin học 10, dữ liệu dạng văn bản khi đưa vào lệnh print bắt buộc đặt trong cặp dấu nháy đơn `' '`. Tuyệt đối không để chữ trần trụi.",
            "Syntax_Missing_Quotes"
        )

    # Trường hợp mở nháy nhưng chưa đóng nháy
    if "unterminated string literal" in error_msg or "EOL while scanning string literal" in error_msg:
        if '"' in code_str:
            return (
                "Chưa đóng dấu nháy kép \" ở cuối xâu kí tự",
                "Văn bản đã mở dấu nháy kép nhưng thiếu dấu nháy kép đóng tương ứng. Bắt buộc thêm dấu nháy kép `\"` ở cuối dòng chữ.",
                "Syntax_Unclosed_Double_Quote"
            )
        return (
            "Chưa đóng dấu nháy đơn ' ở cuối xâu kí tự",
            "Văn bản đã mở dấu nháy đơn nhưng thiếu dấu nháy đơn đóng tương ứng. Bắt buộc thêm dấu nháy đơn `'` ở cuối dòng chữ.",
            "Syntax_Unclosed_Single_Quote"
        )

    # Trường hợp viết hoa chữ Print
    if has_cap_print:
        return (
            "Sai chính tả từ khóa lệnh (Viết hoa chữ P)",
            "Trong Python, tên lệnh phân biệt chữ hoa và chữ thường. Lệnh xuất ra màn hình bắt buộc viết thường toàn bộ là `print`.",
            "Syntax_Print_Capitalized"
        )

    # Quên đóng ngoặc đơn
    if "was never closed" in error_msg or ("(" in code_str and code_str.count("(") > code_str.count(")")):
        return (
            "Thiếu dấu đóng ngoặc đơn )",
            "Mỗi dấu mở ngoặc đơn `(` bắt buộc có một dấu đóng ngoặc đơn `)` tương ứng ở cuối câu lệnh.",
            "Syntax_Unclosed_Paren"
        )

    # Thiếu dấu hai chấm
    if "expected ':'" in error_msg or any(re.match(r'^\s*(if|elif|else|for|while|def)\b', l) and not l.strip().endswith(":") for l in lines):
        return (
            "Thiếu dấu hai chấm : ở cuối câu lệnh điều khiển",
            "Theo quy chuẩn cú pháp SGK Tin học 10, cuối câu lệnh điều khiển bắt buộc kết thúc bằng dấu hai chấm `:`. ",
            "Syntax_Missing_Colon"
        )

    # Thụt lề
    if "IndentationError" in error_msg:
        return (
            "Lỗi cấu trúc thụt lề dòng lệnh",
            "Các câu lệnh con bên trong khối lệnh (sau dấu `:`) bắt buộc thụt lề thống nhất 4 khoảng trắng.",
            "Syntax_Indentation"
        )

    # Nhầm gán = và so sánh ==
    if re.search(r'\bif\b.*(?<!=)=(?!=)', code_str):
        return (
            "Nhầm lẫn giữa phép gán = và phép so sánh bằng ==",
            "Dấu `=` dùng để gán giá trị cho biến. Để so sánh bằng nhau trong mệnh đề điều kiện `if`, bắt buộc dùng cặp dấu `==`.",
            "Misconception_Equal_Operator"
        )

    # Quên ép kiểu input()
    if "input()" in code_str and ("+" in code_str) and ("int(" not in code_str and "float(" not in code_str):
        return (
            "Chưa ép kiểu dữ liệu cho lệnh input()",
            "Lệnh input() luôn trả về dữ liệu kiểu xâu kí tự. Để tính toán cộng trừ số học, bắt buộc sử dụng hàm ép kiểu `int(input())` theo Bài 18 SGK.",
            "Misconception_Type_Casting"
        )

    # Lỗi cú pháp chung: Triệt tiêu hoàn toàn chuỗi perhaps
    if "SyntaxError" in error_msg:
        return (
            "Sai quy chuẩn cú pháp câu lệnh",
            "Câu lệnh vi phạm quy tắc cấu trúc Python. Bắt buộc kiểm tra: từ khóa viết chữ thường, văn bản có cặp dấu nháy đơn `' '` và đóng đủ ngoặc đơn `)`.",
            "Syntax_General"
        )

    # Chưa in kết quả
    if not error_msg and actual_output == "":
        return (
            "Chưa có lệnh in kết quả ra màn hình",
            "Chương trình đã chạy xong nhưng chưa hiển thị dữ liệu. Bắt buộc sử dụng lệnh `print(...)` để xuất kết quả ra màn hình.",
            "Logic_Missing_Print"
        )

    # Sai kết quả tính toán
    if not error_msg and actual_output != expected_output:
        return (
            "Kết quả tính toán chưa chính xác",
            f"Kết quả thực tế là `{actual_output}`, nhưng đề bài yêu cầu chính xác là `{expected_output}`. Em hãy kiểm tra lại biểu thức tính toán.",
            "Logic_Incorrect_Result"
        )

    # Lỗi thực thi khác
    if error_msg:
        return (
            "Lỗi thực thi chương trình",
            "Chương trình phát sinh lỗi khi chạy. Bắt buộc kiểm tra lại kiểu dữ liệu đầu vào và các phép toán.",
            "Runtime_General"
        )

    return ("Chưa đạt yêu cầu", "Em hãy đối chiếu lại đề bài và cấu trúc câu lệnh theo SGK.", "General")

def generate_scaffolding_guidance(attempt_count, diagnosis, exercise):
    title, diag_text, diag_tag = diagnosis
    clean_diag = purge_hedging(diag_text)
    
    generic_syntax = GENERIC_SYNTAX_TEMPLATES.get(
        diag_tag,
        GENERIC_SYNTAX_TEMPLATES["Syntax_General"]
    )
    
    msg = (
        f"🧑‍🏫 **Định hướng chuẩn SGK Tin 10:**\n"
        f"- **Vấn đề phát hiện:** {title}.\n"
        f"- **Quy chuẩn bắt buộc:** {clean_diag}\n"
        f"👉 **Cú pháp chuẩn:**\n"
        f"```python\n{generic_syntax}\n```"
    )
    return purge_hedging(msg)

# ==================== 1. GIAO DIỆN ĐĂNG NHẬP ====================
if not st.session_state.authenticated:
    st.markdown("""
        <div style='background-color: #007bc7; padding: 22px 28px; border-radius: 8px; margin-bottom: 30px; text-align: center; box-shadow: 0 2px 8px rgba(0, 123, 199, 0.15);'>
            <h2 style='color: white; margin: 0; font-size: 1.4rem; font-weight: 700;'>💻 EDUCODER 10 - TRỢ LÝ HỌC LẬP TRÌNH CÁ NHÂN HÓA TIN HỌC 10</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.25, 1])
    with col_l2:
        with st.container(border=True):
            st.markdown("### 🔐 Đăng Nhập Hệ Thống")
            login_id = st.text_input("Tài khoản (Email hoặc Mã học sinh):", placeholder="luyennmhcmue@gmail.com hoặc 10a1_01")
            password = st.text_input("Mật khẩu:", type="password")
            
            if st.button("Đăng nhập", type="primary", use_container_width=True):
                user_data, msg = authenticate_user(login_id.strip(), password.strip())
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.nav_page = "🏠 Trang chủ"
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
    st.stop()

# ==================== 2. GIAO DIỆN CHÍNH (ĐÃ ĐĂNG NHẬP) ====================
user = st.session_state.user
is_teacher = (user.get("role") == "teacher")
clean_name = user['full_name'].replace("Thầy/Cô", "").replace("Cô", "").replace("Thầy", "").strip()

if is_teacher:
    user_tag = f"👨‍🏫 Thầy/Cô {clean_name}"
    nav_options = ["🏠 Trang chủ", "📖 Lý thuyết SGK", "📝 Kho Bài Tập Python", "📊 Báo cáo Benchmark", user_tag]
else:
    class_label = f" ({user.get('class_name')})" if user.get('class_name') else ""
    user_tag = f"👤 {clean_name}{class_label}"
    nav_options = ["🏠 Trang chủ", "📖 Lý thuyết SGK", "📝 Kho Bài Tập Python", user_tag]

st.markdown("""
    <div style='background-color: #007bc7; padding: 14px; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>💻 EDUCODER 10 - TRỢ LÝ HỌC LẬP TRÌNH CÁ NHÂN HÓA TIN HỌC 10</h3>
    </div>
""", unsafe_allow_html=True)

if st.session_state.nav_page not in nav_options:
    st.session_state.nav_page = nav_options[0]

current_idx = nav_options.index(st.session_state.nav_page)
selected_nav = st.radio(
    label="Điều hướng hệ thống",
    options=nav_options,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed"
)

if selected_nav != st.session_state.nav_page:
    st.session_state.nav_page = selected_nav
    st.session_state.doing_exercise = False
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TAB 1: TRANG CHỦ -----------------
if st.session_state.nav_page == "🏠 Trang chủ":
    if not is_teacher:
        st.markdown(f"### Xin chào **{user['full_name']}**!")
        
        with st.container(border=True):
            st.markdown("#### Ma trận Năng lực Lập trình Thực tế của Em")
            st.caption("Chỉ số % thành thạo được tính toán thực tế 100% từ kết quả bài nộp của em trong CSDL.")
            
            competencies = get_student_competencies(user["account_id"])
            cols_comp = st.columns(len(competencies))
            
            for idx, c in enumerate(competencies):
                with cols_comp[idx]:
                    m_val = c["mastery_percent"]
                    st.markdown(f"**{c['topic_prefix']}**")
                    st.caption(f"{c['topic_name']}")
                    st.progress(m_val / 100.0)
                    
                    if m_val >= 80:
                        st.success(f"🏆 {m_val}% (Thành thạo)")
                    elif m_val > 0:
                        st.info(f"⚡ {m_val}% (Đang rèn luyện)")
                    else:
                        st.warning("⚠️ 0.0% (Chưa bắt đầu)")
                    
                    st.caption(f"Đạt: **{c['passed_count']}** bài | Đã nộp: **{c['total_attempts']}** lần")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 🚀 Lộ trình Học tập Thích ứng Hôm nay")
        recommendations = get_adaptive_recommendation(user["account_id"], REAL_EXERCISES)
        cols_rec = st.columns(len(recommendations))
        
        for idx, rec in enumerate(recommendations):
            with cols_rec[idx]:
                with st.container(border=True):
                    st.caption(rec["badge"])
                    st.markdown(f"##### 🎯 Bước {idx + 1}: {rec['type']}")
                    st.write(f"**Bài tập:** `[{rec['exercise']['id']}]` {rec['exercise']['title']}")
                    st.caption(f"**Lý do:** {rec['reason']}")
                    
                    if st.button(f"Luyện bài này ➡️", key=f"btn_rec_{idx}", use_container_width=True, type="primary" if idx == 0 else "secondary"):
                        st.session_state.current_ex_id = rec["exercise"]["id"]
                        st.session_state.doing_exercise = True
                        st.session_state.messages = []
                        st.session_state.nav_page = "📝 Kho Bài Tập Python"
                        st.rerun()

    else:
        st.markdown(f"### 🏠 Bảng điều khiển Giảng dạy - Thầy/Cô {clean_name}")
        st.info("Hệ thống Trợ lý học tập cá nhân hóa EduCoder 10 đang giám sát tiến trình học tập của học sinh.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.markdown("#### 📖 Lý thuyết Tin 10")
                st.write("Bài học cốt lõi theo chương trình GDPT 2018.")
                if st.button("Xem Lý thuyết ➡️", key="btn_t_theory", use_container_width=True):
                    st.session_state.nav_page = "📖 Lý thuyết SGK"
                    st.rerun()
        with c2:
            with st.container(border=True):
                st.markdown("#### 📝 Kho Bài Tập")
                st.write("Ngân hàng bài tập theo mức độ.")
                if st.button("Xem Bài tập ➡️", key="btn_t_practice", use_container_width=True):
                    st.session_state.nav_page = "📝 Kho Bài Tập Python"
                    st.rerun()
        with c3:
            with st.container(border=True):
                st.markdown("#### 📊 Báo cáo Benchmark")
                st.write("Dữ liệu đánh giá thực tế của học sinh.")
                if st.button("Xem Báo cáo ➡️", key="btn_t_bench", use_container_width=True):
                    st.session_state.nav_page = "📊 Báo cáo Benchmark"
                    st.rerun()

# ----------------- TAB 2: LÝ THUYẾT SGK -----------------
elif st.session_state.nav_page == "📖 Lý thuyết SGK":
    st.markdown("### 📖 CỐT LÕI KIẾN THỨC SGK TIN HỌC 10")
    lesson_keys = list(LESSONS_DATA.keys())
    selected_lesson = st.selectbox("Chọn bài học:", lesson_keys, index=15)
    with st.container(border=True):
        st.markdown(f"## 📘 {selected_lesson}")
        st.markdown(LESSONS_DATA[selected_lesson])

# ----------------- TAB 3: KHO BÀI TẬP PYTHON -----------------
elif st.session_state.nav_page == "📝 Kho Bài Tập Python":
    if st.session_state.doing_exercise and st.session_state.current_ex_id:
        curr_ex = next((item for item in REAL_EXERCISES if item["id"] == st.session_state.current_ex_id), REAL_EXERCISES[0])
        
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Quay lại danh sách bài", key="btn_back_list"):
                st.session_state.doing_exercise = False
                st.rerun()

        st.markdown(f"### 💻 LÀM BÀI: [{curr_ex['id']}] {curr_ex['title']}")
        st.caption(f"Trọng tâm kiến thức: **{curr_ex['concept']}**")

        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            with st.container(border=True):
                st.markdown(f"#### 🎯 ĐỀ BÀI: {curr_ex['title']} ({curr_ex['difficulty']})")
                st.write(curr_ex['desc'])

            default_placeholder = f"# Viết mã nguồn cho bài {curr_ex['id']}\n"
            student_code = st.text_area(label="Trình soạn thảo", value=default_placeholder, height=200, label_visibility="collapsed")
            btn_submit = st.button("🚀 Nộp bài & Chấm điểm", type="primary", use_container_width=True)

            if btn_submit:
                all_tests = curr_ex.get("tests", [])
                passed_tests = 0
                test_logs = []
                first_error = ""
                first_actual = ""
                first_expected = ""

                for idx, t in enumerate(all_tests):
                    old_stdin = sys.stdin
                    old_stdout = sys.stdout
                    sys.stdin = io.StringIO(t["input"])
                    buffer = io.StringIO()
                    sys.stdout = buffer
                    
                    err_msg = None
                    try:
                        exec_scope = {}
                        exec(student_code, exec_scope)
                        actual_out = buffer.getvalue().strip()
                    except SyntaxError as se:
                        err_msg = f"SyntaxError: {se.msg} (dòng {se.lineno})"
                    except Exception as e:
                        err_msg = f"{type(e).__name__}: {str(e)}"
                    finally:
                        sys.stdin = old_stdin
                        sys.stdout = old_stdout

                    if err_msg:
                        if not first_error:
                            first_error = err_msg
                        clean_log = re.sub(r"Perhaps you forgot.*", "", err_msg, flags=re.IGNORECASE).strip()
                        test_logs.append(f"Test #{idx + 1}: ❌ Lỗi cú pháp dòng lệnh -> {clean_log}")
                    else:
                        exp_out = str(t["expected"]).strip()
                        if actual_out == exp_out:
                            passed_tests += 1
                            test_logs.append(f"Test #{idx + 1}: ✔️ Chính xác (Kết quả: {actual_out})")
                        else:
                            if not first_actual:
                                first_actual = actual_out
                                first_expected = exp_out
                            test_logs.append(f"Test #{idx + 1}: ❌ Sai kết quả (Nhận được: '{actual_out}', Yêu cầu: '{exp_out}')")

                total_t = len(all_tests)
                score = round((passed_tests / total_t) * 10.0, 1) if total_t > 0 else 0.0

                diag_title, diag_desc, diag_tag = diagnose_student_misconception(
                    student_code, first_error, first_actual, first_expected, curr_ex
                )

                attempt_count = get_exercise_submission_count(user.get('account_id'), curr_ex['id']) + 1
                
                save_submission(
                    user.get('account_id'), 
                    curr_ex['id'], 
                    student_code, 
                    "Passed" if passed_tests == total_t else "Failed", 
                    score, 
                    diag_title if passed_tests < total_t else ""
                )

                if passed_tests == total_t:
                    st.success(f"🎉 Hoàn thành xuất sắc! - {passed_tests}/{total_t} Tests: {score}/10 Điểm")
                    guidance = "🎉 **Chúc mừng em!** Em đã viết chương trình hoàn toàn chính xác theo đúng chuẩn SGK."
                else:
                    st.warning(f"⚠️ Chưa đạt yêu cầu - {passed_tests}/{total_t} Tests: {score}/10 Điểm")
                    guidance = generate_scaffolding_guidance(attempt_count, (diag_title, diag_desc, diag_tag), curr_ex)

                st.session_state.messages.append({"role": "assistant", "content": guidance})
                st.code("\n".join(test_logs), language="text")

                if passed_tests < total_t:
                    with st.container(border=True):
                        st.markdown("##### 🔍 Chẩn đoán Nhận thức chuẩn SGK:")
                        st.info(f"**Vấn đề phát hiện:** {diag_title}\n\n**Quy chuẩn bắt buộc:** {purge_hedging(diag_desc)}")

        with col_right:
            c_head, c_btn_cl = st.columns([3, 1])
            with c_head:
                st.markdown("#### 🤖 Trợ lý Socratic AI")
            with c_btn_cl:
                if st.button("🗑️ Xóa chat", key="btn_clear_chat_active"):
                    st.session_state.messages = []
                    st.rerun()

            with st.container(height=420):
                if not st.session_state.messages:
                    st.caption("Thầy/Cô Trợ lý AI định vị chính xác lỗi cú pháp SGK và định hướng phương pháp, không giải hộ bài.")
                for m in st.session_state.messages:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])

            if user_prompt := st.chat_input("Hỏi AI về quy tắc cú pháp SGK hoặc lỗi câu lệnh..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                bad_words = ["mẹ mày", "đm", "đmm", "vcl", "chó", "vl"]
                if any(bw in user_prompt.lower() for bw in bad_words):
                    if not is_teacher:
                        add_strike(user.get('account_id'))
                    ai_ans = "🚨 **CẢNH BÁO VI PHẠM KỶ LUẬT!** Em bắt buộc phải giữ chuẩn mực văn hóa ứng xử trong giờ học."
                else:
                    p_lower = user_prompt.lower()
                    if "chỉ cách làm" in p_lower or "làm sao" in p_lower or "hướng dẫn" in p_lower or "cú pháp" in p_lower or "dấu" in p_lower:
                        ai_ans = (
                            f"🧑‍🏫 **Quy chuẩn SGK Tin 10:**\n"
                            f"- Yêu cầu: {curr_ex['desc']}\n"
                            f"👉 **Cú pháp chuẩn:**\n"
                            f"```python\nprint('nội_dung_cần_in')\n```"
                        )
                    else:
                        ai_ans = f"🤖 **Trợ lý SGK Tin 10:** Em đang thực hành bài '{curr_ex['title']}'. Hãy nộp bài để hệ thống tự động bóc tách điểm sai và hướng dẫn sửa bằng tiếng Việt."
                
                ai_ans = purge_hedging(ai_ans)
                st.session_state.messages.append({"role": "assistant", "content": ai_ans})
                st.rerun()

    else:
        st.markdown("### 📚 KHO BÀI TẬP PYTHON")
        col_filters, col_detail = st.columns([1.1, 1.3])
        
        with col_filters:
            chap_list = sorted(list(set(e["chapter"] for e in REAL_EXERCISES)))
            selected_chapter = st.selectbox("Chọn chương kiến thức:", chap_list)
            
            diff_options = ["Tất cả", "Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
            selected_diff = st.radio("Mức độ nhận thức:", diff_options, horizontal=True)
            
            filtered_exercises = [
                ex for ex in REAL_EXERCISES 
                if ex["chapter"] == selected_chapter and (selected_diff == "Tất cả" or ex["difficulty"] == selected_diff)
            ]
            
            ex_options = [f"[{ex['id']}] {ex['title']}" for ex in filtered_exercises]
            if ex_options:
                selected_ex_str = st.selectbox("Chọn bài thực hành:", ex_options)
                selected_ex_id = selected_ex_str.split("]")[0].replace("[", "").strip()
                chosen_exercise = next(ex for ex in filtered_exercises if ex["id"] == selected_ex_id)
            else:
                chosen_exercise = None

        with col_detail:
            if chosen_exercise:
                with st.container(border=True):
                    st.markdown(f"#### 📄 {chosen_exercise['title']} ({chosen_exercise['difficulty']})")
                    student_score = get_student_highest_score(user.get('account_id'), chosen_exercise['id'])
                    st.write(f"**Mã bài:** `{chosen_exercise['id']}` | **Điểm cao nhất của bạn:** `{student_score}/10`")
                    st.markdown("##### Yêu cầu đề bài:")
                    st.write(chosen_exercise['desc'])
                    st.markdown("##### Khái niệm trọng tâm:")
                    st.info(chosen_exercise['concept'])
                    st.markdown("##### Dữ liệu kiểm thử mẫu:")
                    for idx, t in enumerate(chosen_exercise.get("tests", [])):
                        inp = str(t.get("input", "")).strip()
                        if inp:
                            st.caption(f"- **Test #{idx + 1}:** Input = `{inp}` ➔ Output = `{t['expected']}`")
                        else:
                            st.caption(f"- **Test #{idx + 1}:** Output = `{t['expected']}`")
                    
                    if st.button("🚀 Bắt đầu làm bài với Trợ lý AI", type="primary", use_container_width=True):
                        st.session_state.current_ex_id = chosen_exercise['id']
                        st.session_state.doing_exercise = True
                        st.session_state.messages = []
                        st.rerun()

# ----------------- TAB 4: BÁO CÁO BENCHMARK -----------------
elif st.session_state.nav_page == "📊 Báo cáo Benchmark" and is_teacher:
    st.markdown("### 📊 BÁO CÁO BENCHMARK")
    
    real_data = get_real_benchmark_report()
    
    if real_data:
        df_bench = pd.DataFrame(real_data)
        
        active_count = len(df_bench[df_bench["total_submissions"] > 0])
        total_subs = int(df_bench["total_submissions"].sum())
        locked_count = len(df_bench[df_bench["status_display"] == "Tạm khóa"])
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("👥 Tổng số học sinh", f"{len(df_bench)} HS (10 Lớp)")
        k2.metric("📝 Học sinh đã làm bài", f"{active_count} HS")
        k3.metric("🚀 Tổng lượt nộp bài", f"{total_subs} lần")
        k4.metric("🛡️ Học sinh vi phạm tạm khóa", f"{locked_count} HS", delta_color="inverse")
        
        st.markdown("---")
        
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            class_list = ["Tất cả các lớp"] + [f"10A{i}" for i in range(1, 11)]
            selected_c = st.selectbox("Lọc theo lớp học:", class_list)
        with col_f2:
            search_name = st.text_input("Tìm kiếm theo Tên hoặc Mã học sinh:", placeholder="Ví dụ: Trần Minh Đức hoặc 10a1_01")

        df_view = df_bench.copy()
        if selected_c != "Tất cả các lớp":
            df_view = df_view[df_view["class_name"] == selected_c]
        if search_name:
            q = search_name.strip().lower()
            df_view = df_view[
                df_view["full_name"].str.lower().str.contains(q) | 
                df_view["account_id"].str.lower().str.contains(q)
            ]

        def format_score(row, field):
            return str(row[field]) if row["total_submissions"] > 0 else "-"

        df_view["highest_display"] = df_view.apply(lambda r: format_score(r, "highest_score"), axis=1)
        df_view["avg_display"] = df_view.apply(lambda r: format_score(r, "avg_score"), axis=1)

        df_display = df_view[[
            "account_id", "full_name", "class_name", "status_display", "total_submissions", "passed_exercises", "highest_display", "avg_display"
        ]].rename(columns={
            "account_id": "Mã học sinh",
            "full_name": "Họ và tên",
            "class_name": "Lớp",
            "status_display": "Trạng thái",
            "total_submissions": "Số lần nộp bài thật",
            "passed_exercises": "Số bài đạt chuẩn (>=8.0)",
            "highest_display": "Điểm cao nhất",
            "avg_display": "Điểm trung bình"
        })
        
        df_display.reset_index(drop=True, inplace=True)
        df_display.index = range(1, len(df_display) + 1)
        df_display.index.name = "STT"
        st.dataframe(df_display, use_container_width=True, height=520)
    else:
        st.info("Chưa có dữ liệu học sinh trong hệ thống.")

# ----------------- TAB 5: HỒ SƠ CÁ NHÂN & ĐỔI MẬT KHẨU -----------------
elif st.session_state.nav_page == user_tag:
    st.markdown(f"### {clean_name}")
    col_p1, col_p2 = st.columns(2)
    
    if is_teacher:
        with col_p1:
            with st.container(border=True):
                st.markdown("#### 📋 Thông tin giảng dạy")
                st.write(f"**Email tài khoản:** `{user.get('email', '')}`")
                st.write(f"**Họ tên Giáo viên:** {clean_name}")
                st.write(f"**Đơn vị phụ trách:** {user.get('class_name', 'Tổ Tin Học')}")

            with st.container(border=True):
                st.markdown("#### 🛡️ Quản lý Kỷ luật & Mở khóa Học sinh")
                locked_list = get_locked_users()
                if locked_list:
                    st.warning(f"⚠️ Hiện có {len(locked_list)} học sinh đang bị khóa.")
                    for s in locked_list:
                        ca, cb = st.columns([3, 1])
                        with ca:
                            st.write(f"👤 **{s['full_name']}** (`{s['account_id']}`) - Lớp: {s.get('class_name', 'N/A')}")
                        with cb:
                            if st.button("🔓 Mở", key=f"unl_{s['id']}"):
                                unlock_user(s['id'])
                                st.success(f"Đã mở khóa cho {s['full_name']}!")
                                st.rerun()
                else:
                    st.success("✅ Không có học sinh nào bị tạm khóa.")

        with col_p2:
            with st.container(border=True):
                st.markdown("#### 🔑 Đổi mật khẩu Thầy/Cô")
                t_old = st.text_input("Mật khẩu hiện tại:", type="password", key="t_old_pwd")
                t_new = st.text_input("Mật khẩu mới:", type="password", key="t_new_pwd")
                t_conf = st.text_input("Xác nhận mật khẩu mới:", type="password", key="t_conf_pwd")
                if st.button("Cập nhật mật khẩu Thầy/Cô", type="primary", use_container_width=True):
                    ident = user.get('email') or user.get('account_id')
                    if t_new == t_conf and change_user_password(ident, t_old, t_new):
                        st.success("Đổi mật khẩu thành công!")
                    else:
                        st.error("Thông tin không chính xác hoặc mật khẩu mới chưa khớp.")
    else:
        with col_p1:
            with st.container(border=True):
                st.markdown("#### 👤 Thông tin Học sinh")
                st.write(f"**Họ và tên:** {user.get('full_name', '')}")
                st.write(f"**Mã số học sinh:** `{user.get('account_id', '')}`")
                st.write(f"**Lớp học:** {user.get('class_name', '10')}")
                st.write(f"**Trạng thái tài khoản:** {user.get('status', 'Bình thường')}")
                st.write(f"**Số lần vi phạm kỷ luật:** `{user.get('strikes', 0)}/3`")
                
                highest_score = get_student_highest_score(user.get('account_id'))
                comps = get_student_competencies(user.get('account_id'))
                total_passed = sum(c['passed_count'] for c in comps)
                total_attempts = sum(c['total_attempts'] for c in comps)
                st.markdown("---")
                st.write(f"**📈 Tổng số lượt nộp bài:** {total_attempts} lần")
                st.write(f"**🏆 Số bài đạt chuẩn (>=8.0):** {total_passed} bài")
                st.write(f"**⭐ Điểm cao nhất đạt được:** {highest_score}/10 điểm")

        with col_p2:
            with st.container(border=True):
                st.markdown("#### 🔑 Đổi mật khẩu Học sinh")
                s_old = st.text_input("Mật khẩu hiện tại:", type="password", key="s_old_pwd")
                s_new = st.text_input("Mật khẩu mới:", type="password", key="s_new_pwd")
                s_conf = st.text_input("Xác nhận mật khẩu mới:", type="password", key="s_conf_pwd")
                if st.button("Cập nhật mật khẩu Học sinh", type="primary", use_container_width=True):
                    ident = user.get('account_id') or user.get('email')
                    if s_new == s_conf and change_user_password(ident, s_old, s_new):
                        st.success("Đổi mật khẩu thành công!")
                    else:
                        st.error("Thông tin không chính xác hoặc mật khẩu mới chưa khớp.")

    st.markdown("---")  
    if st.button("🚪 Đăng Xuất Khỏi Hệ Thống", type="secondary", use_container_width=True):
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.nav_page = "🏠 Trang chủ"
        st.session_state.doing_exercise = False
        st.session_state.messages = []
        st.rerun()