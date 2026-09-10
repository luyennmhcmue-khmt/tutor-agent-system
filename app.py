import io
import sys
import streamlit as st
import pandas as pd
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
    "Bài 24: Xâu ký tự (String)": "### 1. Cấu trúc xâu\n- Xâu đặt trong cặp nháy đơn hoặc nháy kép. Xâu trong Python là đối tượng bất biến.",
    "Bài 25: Thao tác trên xâu ký tự": "### 1. Phương thức xử lý xâu\n- `s.split()`, `s.strip()`, `s.upper()`, `s.lower()`, `s.replace()`.",
    "Bài 26: Hàm trong Python": "### 1. Định nghĩa hàm\n```python\ndef tên_hàm(tham_số):\n    khối_lệnh\n    return giá_trị\n```",
    "Bài 27: Tham số của hàm": "### 1. Tham số & Đối số\n- Hỗ trợ tham số mặc định: `def chao(ten='Bạn'):`",
    "Bài 28: Phạm vi của biến": "### 1. Biến cục bộ & Toàn cục\n- Biến trong hàm là cục bộ. Dùng từ khóa `global` để chỉnh sửa biến bên ngoài hàm.",
    "Bài 29: Nhận biết lỗi chương trình": "### 1. Ba loại lỗi chính\n- `SyntaxError`: Lỗi cú pháp.\n- `RuntimeError`: Lỗi thực thi (chia 0, truy xuất ngoài mảng).\n- `LogicError`: Lỗi sai thuật toán.",
    "Bài 30: Kiểm thử và gỡ lỗi chương trình": "### 1. Kiểm thử & Gỡ lỗi\n- Kiểm tra trường hợp thông thường và trường hợp biên (số 0, số âm, danh sách rỗng)."
}

# ==================== NGÂN HÀNG BÀI TẬP THỰC TẾ CHUẨN SGK TIN 10 ====================
REAL_EXERCISES = [
    {
        "id": "C1_01",
        "chapter": "Chương 1: Vào/Ra & Biến cơ sở",
        "difficulty": "Nhận biết",
        "title": "In dòng chữ xin chào",
        "desc": "Viết chương trình Python in ra màn hình chính xác dòng chữ: `Xin chào Python!`",
        "hint": "Sử dụng hàm: print('Xin chào Python!')",
        "concept": "Lệnh in cơ bản và chuỗi ký tự",
        "tests": [{"input": "", "expected": "Xin chào Python!"}]
    },
    {
        "id": "C1_02",
        "chapter": "Chương 1: Vào/Ra & Biến cơ sở",
        "difficulty": "Thông hiểu",
        "title": "Tính tổng hai số nguyên",
        "desc": "Nhập từ bàn phím hai số nguyên a và b (mỗi số trên một dòng). Tính và in ra tổng của chúng.",
        "hint": "Cần ép kiểu int cho input(): a = int(input()) và b = int(input()). Sau đó print(a + b).",
        "concept": "Ép kiểu dữ liệu số nguyên int(input())",
        "tests": [
            {"input": "5\n7", "expected": "12"},
            {"input": "10\n-3", "expected": "7"}
        ]
    },
    {
        "id": "C1_03",
        "chapter": "Chương 1: Vào/Ra & Biến cơ sở",
        "difficulty": "Vận dụng",
        "title": "Tính diện tích hình chữ nhật",
        "desc": "Nhập chiều dài và chiều rộng (số thực) trên 2 dòng. In ra diện tích của hình chữ nhật.",
        "hint": "Dùng float(input()) để đọc số thực. Diện tích = dài * rộng.",
        "concept": "Ép kiểu dữ liệu số thực float(input())",
        "tests": [
            {"input": "4.5\n2.0", "expected": "9.0"},
            {"input": "10\n5", "expected": "50.0"}
        ]
    },
    {
        "id": "C2_01",
        "chapter": "Chương 2: Rẽ nhánh & Vòng lặp",
        "difficulty": "Nhận biết",
        "title": "Kiểm tra số chẵn lẻ",
        "desc": "Nhập một số nguyên n từ bàn phím. In `CHAN` nếu n là số chẵn, ngược lại in `LE`.",
        "hint": "Dùng phép chia dư n % 2 == 0 kết hợp câu lệnh if/else.",
        "concept": "Cấu trúc rẽ nhánh if-else và toán tử %",
        "tests": [
            {"input": "8", "expected": "CHAN"},
            {"input": "15", "expected": "LE"}
        ]
    },
    {
        "id": "C2_02",
        "chapter": "Chương 2: Rẽ nhánh & Vòng lặp",
        "difficulty": "Thông hiểu",
        "title": "Tìm số lớn hơn trong hai số",
        "desc": "Nhập hai số nguyên a và b trên 2 dòng. In ra giá trị của số lớn hơn.",
        "hint": "Dùng câu lệnh rẽ nhánh if a > b: print(a) else: print(b).",
        "concept": "So sánh logic và rẽ nhánh điều kiện",
        "tests": [
            {"input": "12\n25", "expected": "25"},
            {"input": "99\n40", "expected": "99"}
        ]
    },
    {
        "id": "C2_03",
        "chapter": "Chương 2: Rẽ nhánh & Vòng lặp",
        "difficulty": "Vận dụng cao",
        "title": "Tính tổng dãy số từ 1 đến N",
        "desc": "Nhập số nguyên dương N. Tính và in ra tổng S = 1 + 2 + ... + N.",
        "hint": "Khởi tạo s = 0. Sử dụng vòng lặp for i in range(1, n + 1): s += i. Sau đó print(s).",
        "concept": "Vòng lặp for và hàm range(start, stop)",
        "tests": [
            {"input": "5", "expected": "15"},
            {"input": "10", "expected": "55"}
        ]
    },
    {
        "id": "C3_01",
        "chapter": "Chương 3: Xâu ký tự & Kiểu List",
        "difficulty": "Nhận biết",
        "title": "Độ dài xâu ký tự",
        "desc": "Nhập một xâu ký tự từ bàn phím. In ra số lượng ký tự của xâu đó.",
        "hint": "Dùng s = input() và in ra kết quả của hàm len(s).",
        "concept": "Xử lý xâu cơ bản và hàm len()",
        "tests": [
            {"input": "EduCoder", "expected": "8"},
            {"input": "Tin hoc 10", "expected": "10"}
        ]
    },
    {
        "id": "C3_02",
        "chapter": "Chương 3: Xâu ký tự & Kiểu List",
        "difficulty": "Thông hiểu",
        "title": "Đếm số phần tử chẵn trong danh sách",
        "desc": "Dòng 1 nhập số N. Dòng 2 nhập N số nguyên cách nhau bằng dấu cách. Đếm số lượng các số chẵn.",
        "hint": "Dùng lst = list(map(int, input().split())), duyệt for x in lst và kiểm tra x % 2 == 0.",
        "concept": "Duyệt danh sách List và biến đếm",
        "tests": [
            {"input": "5\n1 2 4 7 8", "expected": "3"},
            {"input": "4\n1 3 5 7", "expected": "0"}
        ]
    },
    {
        "id": "C4_01",
        "chapter": "Chương 4: Hàm & Chương trình con",
        "difficulty": "Thông hiểu",
        "title": "Hàm tính lũy thừa cơ số",
        "desc": "Nhập cơ số a và số mũ b trên 2 dòng. Định nghĩa hàm luy_thua(a, b) và in ra giá trị a mũ b.",
        "hint": "Định nghĩa def luy_thua(a, b): return a ** b. Sau đó gọi print(luy_thua(a, b)).",
        "concept": "Định nghĩa hàm def và lệnh return",
        "tests": [
            {"input": "2\n3", "expected": "8"},
            {"input": "5\n2", "expected": "25"}
        ]
    },
    {
        "id": "C5_01",
        "chapter": "Chương 5: Thuật toán & Gỡ lỗi",
        "difficulty": "Vận dụng cao",
        "title": "Tìm số lớn nhất trong dãy",
        "desc": "Dòng 1 nhập số N. Dòng 2 nhập N số nguyên cách nhau bởi khoảng trắng. In ra phần tử lớn nhất.",
        "hint": "Khởi tạo max_val = lst[0] và duyệt qua danh sách để so sánh cập nhật.",
        "concept": "Thuật toán tìm cực trị Max/Min trên mảng",
        "tests": [
            {"input": "5\n3 9 1 12 7", "expected": "12"},
            {"input": "3\n-5 -2 -9", "expected": "-2"}
        ]
    }
]

# ==================== CHẨN ĐOÁN QUAN NIỆM SAI LẦM ====================
def diagnose_student_misconception(student_code, error_msg, actual_output, expected_output, exercise):
    code_str = student_code.strip()
    if "SyntaxError" in error_msg:
        if "was never closed" in error_msg or ("(" in code_str and code_str.count("(") > code_str.count(")")):
            return ("Quên đóng ngoặc đơn `)`", "Em đang mở ngoặc `(` nhưng quên đóng dấu `)` ở cuối câu lệnh.", "Syntax_Unclosed_Paren")
        if "expected ':'" in error_msg or ("if " in code_str and ":" not in code_str):
            return ("Thiếu dấu hai chấm `:`", "Sau câu lệnh if, else, for, while, def bắt buộc phải kết thúc bằng dấu hai chấm `:`. Em hãy bổ sung nhé!", "Syntax_Missing_Colon")
        return ("Sai cú pháp câu lệnh", f"Chương trình gặp lỗi: {error_msg}. Em hãy kiểm tra lại chính tả từ khóa.", "Syntax_General")
        
    if exercise["id"] in ["C1_02", "C1_03"]:
        if "input()" in code_str and "int(" not in code_str and "float(" not in code_str:
            return ("Quên ép kiểu int() / float()", "Hàm `input()` mặc định trả về chuỗi văn bản. Khi em cộng `a + b`, Python sẽ nối hai chuỗi lại với nhau thay vì tính tổng số học. Em hãy dùng `int(input())` nhé!", "Misconception_Type_Casting")

    if "if " in code_str and "=" in code_str and "==" not in code_str and "!=" not in code_str and ">" not in code_str and "<" not in code_str:
        return ("Nhầm giữa phép gán `=` và so sánh `==`", "Dấu `=` dùng để gán giá trị cho biến. Để so sánh bằng nhau trong câu lệnh if, em phải dùng hai dấu bằng `==`.", "Misconception_Equal_Operator")

    if not error_msg:
        if actual_output == "":
            return ("Chưa xuất kết quả ra màn hình", "Chương trình chưa in kết quả. Em hãy dùng lệnh `print(...)` để xuất kết quả ra màn hình nhé!", "Logic_Missing_Print")
        return ("Kết quả chưa chính xác", f"Kết quả nhận được là `{actual_output}`, yêu cầu đúng là `{expected_output}`. Em hãy kiểm tra lại phép tính.", "Logic_Incorrect_Result")

    return ("Lỗi thực thi", f"Lỗi: {error_msg}", "Runtime_General")

def generate_scaffolding_guidance(attempt_count, diagnosis, exercise):
    title, diag_text, _ = diagnosis
    if attempt_count == 1:
        return f"🧑‍🏫 **Gợi ý phản tư (Lần nộp 1):**\n- Em đang gặp vấn đề: **{title}**.\n- {diag_text}\n👉 Hãy thử quan sát lại câu lệnh và sửa lại nhé!"
    elif attempt_count == 2:
        return f"🧑‍🏫 **Định vị điểm nghẽn (Lần nộp 2):**\n- Vấn đề: **{title}**.\n- {diag_text}\n💡 **Gợi ý phương pháp:** `{exercise['hint']}`"
    else:
        return f"🧑‍🏫 **Giàn giáo tư duy (Lần nộp {attempt_count}):**\n- Em hãy làm theo 3 bước:\n  1. Nhập dữ liệu và ép kiểu đúng yêu cầu.\n  2. Thực hiện phép toán: `{exercise['hint']}`.\n  3. Dùng lệnh `print(...)` xuất kết quả."

# ==================== 1. GIAO DIỆN ĐĂNG NHẬP ====================
if not st.session_state.authenticated:
    st.markdown("""
        <div style='background-color: #0284c7; padding: 16px; border-radius: 8px; margin-bottom: 25px;'>
            <h2 style='color: white; margin: 0; text-align: center;'>💻 EDUCODER 10 - TRỢ LÝ HỌC LẬP TRÌNH CÁ NHÂN HÓA TIN HỌC 10</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
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
    <div style='background-color: #0284c7; padding: 14px; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>💻 EDUCODER 10 - TRỢ LÝ HỌC LẬP TRÌNH CÁ NHÂN HÓA TIN HỌC 10 (GDPT 2018)</h3>
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

# ----------------- TAB 1: TRANG CHỦ (MA TRẬN NĂNG LỰC THỰC TẾ) -----------------
if st.session_state.nav_page == "🏠 Trang chủ":
    if not is_teacher:
        st.markdown(f"### 🎯 Xin chào **{user['full_name']}**! Bảng điều khiển Trợ lý Cá nhân hóa")
        
        with st.container(border=True):
            st.markdown("#### 📊 Năng lực Lập trình cá nhân")
            
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

        st.markdown("#### Lộ trình Học tập Hôm nay")
        st.caption("Dựa trên tiến độ bài làm và các lỗ hổng kiến thức đã được ghi nhận, Trợ lý AI thiết kế lộ trình 3 bước:")
        
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
                        st.session_state.nav_page = "Kho Bài Tập Python"
                        st.rerun()

    else:
        st.markdown(f"### 🏠 Bảng điều khiển Giảng dạy - Thầy/Cô {clean_name}")
        st.info("Hệ thống Trợ lý học tập cá nhân hóa EduCoder 10 đang giám sát tiến trình học tập của học sinh.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.markdown("#### 📖 Lý thuyết Tin học 10")
                st.write("Bài học cốt lõi theo chương trình GDPT 2018.")
                if st.button("Xem Lý thuyết ➡️", key="btn_t_theory", use_container_width=True):
                    st.session_state.nav_page = "📖 Lý thuyết SGK"
                    st.rerun()
        with c2:
            with st.container(border=True):
                st.markdown("#### 📝 Kho Bài Tập Python")
                st.write("Ngân hàng các bài tập theo mức độ nhận biết.")
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

# ----------------- TAB 2: LÝ THUYẾT SGK (30 BÀI) -----------------
elif st.session_state.nav_page == "📖 Lý thuyết SGK":
    st.markdown("### 📖 CỐT LÕI KIẾN THỨC SGK TIN HỌC 10")
    lesson_keys = list(LESSONS_DATA.keys())
    selected_lesson = st.selectbox("Chọn bài học:", lesson_keys, index=15)
    with st.container(border=True):
        st.markdown(f"## 📘 {selected_lesson}")
        st.markdown(LESSONS_DATA[selected_lesson])

# ----------------- TAB 3: KHO BÀI TẬP PYTHON & CHẤM ĐIỂM CÁ NHÂN HÓA -----------------
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
                st.caption(f"💡 **Gợi ý phương pháp:** {curr_ex['hint']}")

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
                    # Mock stdin và stdout chống treo khi có input()
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
                        test_logs.append(f"Test #{idx + 1}: ❌ Lỗi thực thi -> {err_msg}")
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
                
                # Lưu vào CSDL và tự động tính toán lại ma trận năng lực thật
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
                    st.toast("🌟 Năng lực thực tế của em đã được cập nhật thành công!")
                    guidance = "🎉 **Chúc mừng em!** Em đã giải quyết bài toán hoàn toàn chính xác. Năng lực của em trong Ma trận đã được cộng điểm thực tế!"
                else:
                    st.warning(f"⚠️ Chưa đạt yêu cầu - {passed_tests}/{total_t} Tests: {score}/10 Điểm")
                    guidance = generate_scaffolding_guidance(attempt_count, (diag_title, diag_desc, diag_tag), curr_ex)

                st.session_state.messages.append({"role": "assistant", "content": guidance})
                st.code("\n".join(test_logs), language="text")

                if passed_tests < total_t:
                    with st.container(border=True):
                        st.markdown("##### 🔍 Chẩn đoán Nhận thức từ Trợ lý Sư phạm:")
                        st.info(f"**Vấn đề phát hiện:** {diag_title}\n\n**Lời khuyên:** {diag_desc}")

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
                    st.caption("Thầy/Cô Trợ lý AI sẵn sàng định vị lỗi nhận thức và gợi mở phương pháp giải giúp em đạt 10/10 điểm!")
                for m in st.session_state.messages:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])

            if user_prompt := st.chat_input("Hỏi AI về phương pháp giải hoặc nguyên lý..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                bad_words = ["mẹ mày", "đm", "đmm", "vcl", "chó", "vl"]
                if any(bw in user_prompt.lower() for bw in bad_words):
                    if not is_teacher:
                        add_strike(user.get('account_id'))
                    ai_ans = "🚨 **CẢNH BÁO VI PHẠM KỶ LUẬT!** Em cần giữ chuẩn mực văn hóa ứng xử trong giờ học."
                else:
                    p_lower = user_prompt.lower()
                    if "chỉ cách làm" in p_lower or "làm sao" in p_lower or "hướng dẫn" in p_lower:
                        ai_ans = f"🧑‍🏫 **Phương pháp giải bài [{curr_ex['id']}]:**\n\n- Yêu cầu: {curr_ex['desc']}\n- Gợi ý: `{curr_ex['hint']}`\nEm hãy tự tay viết lệnh theo gợi ý nhé!"
                    else:
                        ai_ans = f"🤖 **Trợ lý gợi ý:** Em đang thực hành bài '{curr_ex['title']}'. Hãy nộp bài để Thầy/Cô tự động chẩn đoán điểm nghẽn giúp em!"

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
                        st.caption(f"- **Test #{idx + 1}:** Input = `{t['input'] if t['input'] else '(không có)'}` ➔ Output = `{t['expected']}`")
                    
                    if st.button("🚀 Bắt đầu làm bài với Trợ lý AI", type="primary", use_container_width=True):
                        st.session_state.current_ex_id = chosen_exercise['id']
                        st.session_state.doing_exercise = True
                        st.session_state.messages = []
                        st.rerun()

# ----------------- TAB 4: BÁO CÁO BENCHMARK (DỮ LIỆU THỰC TẾ 100% CHO GIÁO VIÊN) -----------------
elif st.session_state.nav_page == "📊 Báo cáo Benchmark" and is_teacher:
    st.markdown("### 📊 BÁO CÁO BENCHMARK THỰC TẾ TOÀN KHỐI 10")
    
    real_data = get_real_benchmark_report()
    
    if real_data:
        df_bench = pd.DataFrame(real_data)
        
        # Thống kê KPI thực tế
        active_count = len(df_bench[df_bench["total_submissions"] > 0])
        total_subs = int(df_bench["total_submissions"].sum())
        avg_score_all = round(df_bench[df_bench["total_submissions"] > 0]["avg_score"].mean(), 1) if active_count > 0 else 0.0
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("👥 Tổng số học sinh", f"{len(df_bench)} HS (10 Lớp)")
        k2.metric("📝 Học sinh đã làm bài thật", f"{active_count} HS")
        k3.metric("🚀 Tổng lượt nộp bài thực tế", f"{total_subs} lần")
        k4.metric("🎯 Điểm TB của HS đã nộp", f"{avg_score_all}/10")
        
        st.markdown("---")
        
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            class_list = ["Tất cả các lớp"] + [f"10A{i}" for i in range(1, 11)]
            selected_c = st.selectbox("Lọc theo lớp học:", class_list)
        with col_f2:
            search_name = st.text_input("Tìm kiếm theo Tên hoặc Mã học sinh:", placeholder="Ví dụ: Trần Minh Đức hoặc 10a1_01")

        # Lọc dữ liệu
        df_view = df_bench.copy()
        if selected_c != "Tất cả các lớp":
            df_view = df_view[df_view["class_name"] == selected_c]
        if search_name:
            q = search_name.strip().lower()
            df_view = df_view[
                df_view["full_name"].str.lower().str.contains(q) | 
                df_view["account_id"].str.lower().str.contains(q)
            ]

        # Trình bày bảng chuẩn hóa
        df_display = df_view[[
            "account_id", "full_name", "class_name", "passed_exercises", "total_submissions", "highest_score", "avg_score", "status"
        ]].rename(columns={
            "account_id": "Mã học sinh",
            "full_name": "Họ và tên",
            "class_name": "Lớp",
            "passed_exercises": "Số bài đạt chuẩn (>=8.0)",
            "total_submissions": "Số lần nộp bài thật",
            "highest_score": "Điểm cao nhất",
            "avg_score": "Điểm trung bình",
            "status": "Trạng thái"
        })
        
        df_display.reset_index(drop=True, inplace=True)
        df_display.index = range(1, len(df_display) + 1)
        df_display.index.name = "STT"
        st.dataframe(df_display, use_container_width=True, height=520)
        st.caption("Dữ liệu được cập nhật tự động từ các bài nộp trong hệ thống.")
    else:
        st.info("Chưa có dữ liệu học sinh trong hệ thống.")

# ----------------- TAB 5: HỒ SƠ CÁ NHÂN & PHÂN QUYỀN -----------------
elif st.session_state.nav_page == user_tag:
    st.markdown(f"### ⚙️ QUẢN TRỊ: {clean_name}")
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
                                unlock_user(s['account_id'])
                                st.success(f"Đã mở khóa thành công cho {s['full_name']}!")
                                st.rerun()
                else:
                    st.info("👍 Không có học sinh nào đang bị khóa.")

        with col_p2:
            with st.container(border=True):
                st.markdown("#### 🔑 Đổi mật khẩu Giáo viên")
                t_old = st.text_input("Mật khẩu hiện tại:", type="password", key="t_old_pwd")
                t_new = st.text_input("Mật khẩu mới:", type="password", key="t_new_pwd")
                t_conf = st.text_input("Xác nhận mật khẩu mới:", type="password", key="t_conf_pwd")
                if st.button("Cập nhật mật khẩu Thầy/Cô", type="primary", use_container_width=True):
                    ident = user.get('email') or user.get('account_id')
                    if t_new == t_conf and change_user_password(ident, t_old, t_new):
                        st.success("Đổi mật khẩu thành công!")
                    else:
                        st.error("Thông tin không chính xác.")
    else:
        with col_p1:
            with st.container(border=True):
                st.markdown("#### 👤 Thông tin Học sinh")
                st.write(f"**Họ và tên:** {user.get('full_name', '')}")
                st.write(f"**Mã số:** `{user.get('account_id', '')}` | **Lớp:** {user.get('class_name', '10')}")
                st.write(f"**Trạng thái:** {user.get('status', 'Bình thường')} | **Số lần vi phạm:** `{user.get('strikes', 0)}/3`")

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
                        st.error("Thông tin không chính xác.")

    st.markdown("---")
    if st.button("🚪 Đăng Xuất Khỏi Hệ Thống", type="secondary"):
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.nav_page = "🏠 Trang chủ"
        st.rerun()