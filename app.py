import io
import sys
import re
import random
import builtins
import sqlite3
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
if "show_test_runner" not in st.session_state:
    st.session_state.show_test_runner = True

# ==================== ĐỊNH DẠNG GIAO DIỆN CHUẨN MẪU ====================
st.markdown("""
<style>
div.st-key-btn_submit_main button {
    background-color: #f0ad4e !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    border: none !important;
    height: 42px !important;
}
div.st-key-btn_toggle_runner button {
    background-color: #449d44 !important;
    color: white !important;
    border: 2px solid #1e5a1e !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    height: 42px !important;
}
div.st-key-btn_run_action button {
    background-color: #5cb85c !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 8px 30px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-green-box) {
    border: 2px solid #7bc143 !important;
    border-radius: 24px !important;
    padding: 16px 20px !important;
    background-color: #fcfdfa !important;
    margin-top: 15px !important;
    margin-bottom: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== DỮ LIỆU LÝ THUYẾT 30 BÀI SGK TIN HỌC 10 ====================
LESSONS_DATA = {
    "Bài 1: Thông tin và xử lý thông tin": "### 1. Thông tin và dữ liệu\n- Dữ liệu: Số liệu, văn bản, âm thanh lưu trữ trên máy tính.\n- Đơn vị đo: Bit, Byte (1B = 8 bits), KB, MB, GB, TB.",
    "Bài 2: Vai trò của thiết bị thông minh và tin học": "### 1. Thiết bị thông minh\n- Tự động kết nối và xử lý thông tin (Smartphone, Robot, Smart TV).",
    "Bài 3: Một số kiểu kiến trúc máy tính": "### 1. Kiến trúc Von Neumann\n- Gồm: CPU, Bộ nhớ trong (RAM, ROM), Hệ thống Vào/Ra, Bus liên kết.",
    "Bài 4: Mạng máy tính và Internet": "### 1. Mạng máy tính & Internet\n- Mạng toàn cầu Internet sử dụng giao thức TCP/IP, định danh qua địa chỉ IP.",
    "Bài 5: Dữ liệu trong máy tính và hệ số": "### 1. Hệ nhị phân (Binary)\n- Cơ số 2 gồm 0 và 1. Dùng bảng mã ASCII và Unicode (UTF-8) để mã hóa văn bản tiếng Việt.",
    "Bài 6: Dữ liệu âm thanh và hình ảnh": "### 1. Số hóa đa phương tiện\n- Điểm ảnh pixel (RGB). Âm thanh được lấy mẫu lượng tử hóa thành chuỗi bit.",
    "Bài 7: Phần mềm đồ họa Vector": "### 1. Đồ họa Vector (Inkscape)\n- Dựa trên công thức toán học, không bị vỡ nét khi phóng to co giãn kích thước.",
    "Bài 8: Định dạng văn bản và bảng biểu nâng cao": "### 1. Kỹ năng văn bản\n- Ngắt trang (Page Break), ngắt phần (Section Break), mục lục tự động, Header/Footer.",
    "Bài 9: Sử dụng bảng tính điện tử nâng cao": "### 1. Công thức bảng tính\n- Địa chỉ tương đối (A1), tuyệt đối ($A$1), hỗn hợp ($A1). Các hàm SUM, AVERAGE, IF, COUNTIF.",
    "Bài 10: Trình diễn đa phương tiện": "### 1. Thiết kế trang chiếu\n- Độ tương phản, phân cấp thông tin thị giác, hiệu ứng slide hợp lý.",
    "Bài 11: An toàn thông tin và bản quyền": "### 1. An toàn không gian mạng\n- Phòng chống virus, Ransomware, Phishing. Tôn trọng bản quyền phần mềm mã nguồn mở.",
    "Bài 12: Đạo đức, pháp luật môi trường số": "### 1. Ứng xử văn hóa số\n- Bảo vệ thông tin cá nhân, ứng xử văn minh trên không gian mạng.",
    "Bài 13: Cơ sở dữ liệu và hệ quản trị CSDL": "### 1. Khái niệm CSDL\n- CSDL lưu trữ dữ liệu có cấu trúc; hệ quản trị DBMS (SQLite, MySQL) xử lý truy vấn.",
    "Bài 14: Dịch vụ đám mây và IoT": "### 1. Đám mây & IoT\n- Cloud cung cấp tài nguyên trực tuyến; IoT kết nối vạn vật qua cảm biến.",
    "Bài 15: Trí tuệ nhân tạo (AI)": "### 1. Bản chất AI\n- Ngành khoa học máy tính mô phỏng quá trình tư duy, học tập và suy luận của con người.",
    "Bài 16: Ngôn ngữ lập trình bậc cao và Python": "### 1. Giới thiệu Python\n- Ngôn ngữ bậc cao, thông dịch, cú pháp rõ ràng.\n- Lệnh in ra màn hình: `print('Xin chào Python!')`",
    "Bài 17: Biến và lệnh gán": "### 1. Biến & Kiểu dữ liệu\n- Tên biến không chứa dấu cách, không bắt đầu bằng chữ số.\n- Kiểu dữ liệu cơ bản: `int`, `float`, `str`, `bool`.\n- Phép toán: `+`, `-`, `*`, `/`, `//` (chia nguyên), `%` (chia dư).",
    "Bài 18: Các lệnh vào ra đơn giản": "### 1. Nhập và xuất dữ liệu\n- Nhập chuỗi: `s = input()`\n- Nhập số nguyên: `n = int(input())`\n- Nhập số thực: `x = float(input())`\n- Xuất dữ liệu: `print(giá_trị)`",
    "Bài 19: Câu lệnh rẽ nhánh if": "### 1. Cú pháp rẽ nhánh\n```python\nif điều_kiện:\n    khối_lệnh\n```\nLưu ý: Bắt buộc thụt lề 4 khoảng trắng.",
    "Bài 20: Câu lệnh lặp for": "### 1. Vòng lặp for\n```python\nfor i in range(n):\n    khối_lệnh\n```",
    "Bài 21: Câu lệnh lặp while": "### 1. Vòng lặp while\n```python\nwhile điều_kiện:\n    khối_lệnh\n```",
    "Bài 22: Kiểu dữ liệu danh sách (List)": "### 1. Khởi tạo danh sách\n`a = [10, 20, 30]`. Phần tử đầu: `a[0]`, phần tử cuối: `a[-1]`.",
    "Bài 23: Thao tác trên dữ liệu danh sách": "### 1. Phương thức danh sách\n- `len(a)`, `a.append(x)`, `a.remove(x)`, `a.sort()`.",
    "Bài 24: Xâu ký tự (String)": "### 1. Cấu trúc xâu\n- Xâu đặt trong cặp dấu nháy đơn `'...'`.",
    "Bài 25: Thao tác trên xâu ký tự": "### 1. Phương thức xử lý xâu\n- `s.split()`, `s.strip()`, `s.upper()`, `s.lower()`.",
    "Bài 26: Hàm trong Python": "### 1. Định nghĩa hàm\n```python\ndef tên_hàm(tham_số):\n    khối_lệnh\n    return giá_trị\n```",
    "Bài 27: Tham số của hàm": "### 1. Tham số & Đối số\n- Hỗ trợ tham số mặc định: `def chao(ten='Bạn'):`",
    "Bài 28: Phạm vi của biến": "### 1. Biến cục bộ & Toàn cục\n- Biến trong hàm là cục bộ. Dùng `global` để chỉnh sửa biến ngoài hàm.",
    "Bài 29: Nhận biết lỗi chương trình": "### 1. Ba loại lỗi chính\n- `SyntaxError`, `RuntimeError`, `LogicError`.",
    "Bài 30: Kiểm thử và gỡ lỗi chương trình": "### 1. Kiểm thử\n- Kiểm tra trường hợp thông thường và trường hợp biên."
}

# ==================== BỘ VIỆT HÓA LỖI HỆ THỐNG (TUYỆT ĐỐI KHÔNG DÙNG 'HOẶC', 'HAY') ====================
def translate_system_error(err_str: str) -> str:
    if not err_str:
        return ""
    err_lower = err_str.lower()
    m_line = re.search(r"dòng (\d+)|line (\d+)", err_str)
    line_str = f" tại dòng {m_line.group(1) or m_line.group(2)}" if m_line else ""
    
    if "invalid syntax" in err_lower or "syntaxerror" in err_lower:
        return f"Sai quy tắc ngữ pháp câu lệnh{line_str}."
    if "can't multiply sequence" in err_lower or "unsupported operand" in err_lower:
        return "Sai kiểu dữ liệu: Dữ liệu từ lệnh input() là xâu văn bản, bắt buộc ép kiểu số trước khi tính toán."
    if "invalid literal for int" in err_lower:
        return "Sai kiểu dữ liệu: Dữ liệu nhập vào chứa số thập phân, bắt buộc dùng hàm float(input())."
    if "nameerror" in err_lower:
        m = re.search(r"name '([^']+)' is not defined", err_str)
        var_name = f"`{m.group(1)}`" if m else "biến"
        return f"Biến {var_name} chưa được tạo giá trị trước khi gọi."
    if "was never closed" in err_lower or "unclosed" in err_lower:
        if "(" in err_lower:
            return "Câu lệnh thiếu dấu đóng ngoặc đơn `)`."
        return "Xâu văn bản thiếu dấu đóng nháy đơn `'`."
    if "unterminated string" in err_lower or "eol while scanning" in err_lower:
        return "Xâu văn bản chưa đóng dấu nháy đơn `'` ở cuối dòng."
    if "zerodivisionerror" in err_lower:
        return "Phép toán chia cho số 0 vi phạm quy tắc toán học."
    if "indentationerror" in err_lower:
        return "Khối lệnh viết sai thụt lề 4 khoảng trắng."
        
    return "Câu lệnh dừng đột ngột do vi phạm cấu trúc SGK."

# ==================== HÀM SO KHỚP KẾT QUẢ THÔNG MINH ====================
def is_output_semantically_correct(actual_out: str, expected_out: str) -> bool:
    act = actual_out.strip()
    exp = expected_out.strip()
    
    if act == exp:
        return True
    
    try:
        exp_float = float(exp)
        found_numbers = re.findall(r'[-+]?\d*\.?\d+', act)
        for num_str in found_numbers:
            try:
                if float(num_str) == exp_float:
                    return True
            except ValueError:
                continue
    except ValueError:
        if exp.lower() in act.lower():
            return True

    return False

# ==================== ĐỘNG CƠ HƯỚNG DẪN TƯ DUY TỪNG BƯỚC ====================
def get_step_by_step_scaffolding(exercise_info: dict, diag_tag: str, error_msg: str) -> str:
    if diag_tag == "NameError":
        m_name = re.search(r"name '([^']+)' is not defined", error_msg)
        var_n = f"'{m_name.group(1)}'" if m_name else "biến"
        return f"💡 **Lỗi cụ thể:** Biến {var_n} chưa được khai báo. Em bắt buộc phải viết câu lệnh gán giá trị từ bàn phím `input()` cho biến này ở phía trên trước khi sử dụng."
    if diag_tag == "Print_Extra_Text":
        return "💡 **Lỗi cụ thể:** Thuật toán tính toán chính xác nhưng lệnh print in thừa lời dẫn văn bản. Máy chấm tự động yêu cầu kết quả phải trần trụi (chỉ in giá trị số)."
    if diag_tag == "Type_Casting_Error":
        return "💡 **Lỗi cụ thể:** Chưa bọc hàm ép kiểu `int()` hoặc `float()` bao quanh lệnh `input()`."
    if diag_tag == "Variable_Naming_Space":
        return "💡 **Lỗi cụ thể:** Tên biến chứa khoảng trắng (dấu cách). Em bắt buộc viết liền và dùng dấu gạch dưới `_`."
    if diag_tag == "Syntax_Missing_Quotes" or diag_tag == "Syntax_Print_Capitalized":
        return "💡 **Lỗi cụ thể:** Viết sai chính tả lệnh `print` hoặc thiếu cặp dấu nháy đơn `' '`."
    if diag_tag == "IndentationError":
        return "💡 **Lỗi cụ thể:** Sai quy tắc thụt lề khối lệnh (bắt buộc đúng chuẩn 4 khoảng trắng)."
    if diag_tag == "Anti_Hardcode_Violation":
        return "💡 **Lỗi cụ thể:** Chưa sử dụng lệnh `input()` để đọc dữ liệu biến thiên từ bàn phím."

    return "💡 **Lỗi cụ thể:** Kết quả thực thi chưa khớp với bộ kiểm thử. Em hãy kiểm tra lại biểu thức tính toán và tên biến."

# ==================== TRỢ LÝ AI TRÒ CHUYỆN & HỎI ĐÁP TOÀN DIỆN ====================
def generate_conversational_ai_response(prompt: str, curr_ex: dict, student_code: str) -> str:
    p = prompt.lower()
    ex_title = curr_ex.get('title', '')
    ex_desc = curr_ex.get('desc', '')
    
    if any(w in p for w in ["chào", "hello", "hi", "cô ơi", "thầy ơi", "giúp em"]):
        return f"Chào em! Thầy/Cô là Trợ lý Socratic AI. Em đang làm bài **'{ex_title}'**. Em đang gặp vướng mắc cụ thể ở dòng code nào, cứ nói cho thầy/cô biết nhé!"
    
    if "input" in p or "nhập" in p:
        return (
            "💡 **Giải đáp về lệnh input():**\n"
            "- Hàm `input()` nhận dữ liệu bàn phím và trả về xâu kí tự (`str`).\n"
            "- Tính toán số học bắt buộc bọc trong `int(input())` hoặc `float(input())`."
        )
        
    if "print" in p or "in" in p:
        return (
            "💡 **Giải đáp về lệnh print():**\n"
            "- Lệnh `print()` xuất kết quả ra màn hình.\n"
            "- Cú pháp chuẩn: `print(giá_trị)`."
        )

    return (
        f"🤖 **Trợ lý Socratic AI:** Thầy/Cô đã ghi nhận câu hỏi của em về bài **'{ex_title}'**.\n"
        f"Mã nguồn hiện tại của em:\n```python\n{student_code}\n```\n"
        f"👉 **Gợi ý hỗ trợ:** Em hãy kiểm tra kỹ các biến đã được gán giá trị qua `input()` chưa, công thức toán học đã đúng chưa và lệnh `print()` đã in trần trụi chưa. Em cần thầy/cô soi giúp đoạn code cụ thể nào không?"
    )

# ==================== BỘ LỌC TỪ NGỮ THÔ TỤC & KHÓA TỨC THÌ ====================
PROFANITY_LIST = [
    "mẹ mày", "đm", "đmm", "vcl", "chó", "vl", "đĩ", "khùng", "đụ", "dkm", "clm",
    "cặc", "lồn", "buồi", "óc chó", "đĩ khùng", "thằng chó", "mẹ m", "con mẹ",
    "bố mày", "thằng điên", "đĩ mẹ", "mẹ kiếp", "đụ mẹ", "địt"
]

def check_profanity(text: str) -> bool:
    t = text.lower()
    for word in PROFANITY_LIST:
        if word in t:
            return True
    return False

# ==================== ĐỘNG CƠ THẨM ĐỊNH THỰC THI AN TOÀN ====================
def execute_student_script(student_code: str, test_input_str: str) -> tuple[str, str]:
    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(test_input_str)
    buffer = io.StringIO()
    sys.stdout = buffer

    def isolated_input(prompt=""):
        line = sys.stdin.readline()
        return line.rstrip("\r\n")

    err_msg = ""
    out_res = ""
    try:
        builtins_dict = builtins.__dict__.copy()
        builtins_dict["input"] = isolated_input
        exec_scope = {"__builtins__": builtins_dict}
        exec(student_code, exec_scope)
        out_res = buffer.getvalue().strip()
    except SyntaxError as se:
        err_msg = f"SyntaxError: {se.msg} (dòng {se.lineno})"
    except Exception as ex:
        err_msg = f"{type(ex).__name__}: {str(ex)}"
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout

    return out_res, err_msg

# ==================== ĐỘNG CƠ CHẨN ĐOÁN SƯ PHẠM (TUYỆT ĐỐI KHÔNG DÙNG 'HOẶC', 'HAY') ====================
HEDGING_PATTERNS = [r"\bcó thể\b", r"\bcó lẽ\b", r"\bdường như\b", r"\bhình như\b", r"\bchắc là\b", r"\bđoán là\b"]

def purge_hedging(text: str) -> str:
    res = text
    for p in HEDGING_PATTERNS:
        res = re.sub(p, "bắt buộc", res, flags=re.IGNORECASE)
    return res.strip()

def diagnose_student_misconception(student_code, error_msg, actual_output, exercise, passed_tests, total_tests):
    code_str = student_code.strip()
    lines = code_str.splitlines()
    tests = exercise.get("tests", [])
    desc_str = (exercise.get("desc", "") + " " + exercise.get("title", "")).lower()
    has_input_req = any(bool(t.get("input", "").strip()) for t in tests) or ("nhập" in desc_str and "không cần nhập" not in desc_str)

    non_comment_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]
    if not non_comment_lines:
        return ("Chưa viết mã nguồn chương trình", "Trình soạn thảo chưa có câu lệnh Python nào để thực thi.", "Syntax_General")

    for l_num, line in enumerate(lines, 1):
        clean_l = line.strip()
        if "=" in clean_l and not any(k in clean_l for k in ["==", "<=", ">=", "!=", "if ", "elif ", "while "]) and not clean_l.startswith("#"):
            left_side = clean_l.split("=")[0].strip()
            if " " in left_side and "," not in left_side and "[" not in left_side and "(" not in left_side:
                return ("Tên biến chứa khoảng trắng", f"Tại dòng {l_num}: Tên biến `{left_side}` chứa dấu cách không hợp lệ.", "Variable_Naming_Space")

    if "input(" in code_str:
        m_var = re.search(r'([a-zA-Z0-9_À-ỹ]+)\s*=\s*(?:[a-zA-Z0-9_]+\()?input\(', code_str)
        if m_var:
            assigned_var = m_var.group(1)
            m_print_str = re.search(r'print\s*\(\s*([\'"][^\'"]+[\'"])\s*\)', code_str)
            if m_print_str and assigned_var not in m_print_str.group(1):
                return ("In xâu cố định thay vì in biến", f"Lệnh print in xâu cố định thay vì biến `{assigned_var}`.", "Print_Literal_Instead_Of_Var")

    has_print_call = bool(re.search(r'\b(print|Print|PRINT)\b', code_str))
    missing_quotes = False
    if has_print_call:
        for line in lines:
            m = re.search(r'(?:print|Print|PRINT)\s*\((.*)\)', line)
            if m:
                inside = m.group(1).strip()
                if inside and ("'" not in inside and '"' not in inside):
                    if re.search(r'[a-zA-Z_À-ỹ]+\s+[a-zA-Z_À-ỹ]+', inside):
                        missing_quotes = True
                        break

    has_cap_print = bool(re.search(r'\b(Print|PRINT)\b', code_str))
    if missing_quotes and has_cap_print:
        return ("Lệnh print viết hoa và thiếu nháy đơn", "Tên lệnh phải là print và xâu trong nháy.", "Syntax_Missing_Quotes")
    if missing_quotes:
        return ("Thiếu cặp dấu nháy đơn ' '", "Văn bản trong print bắt buộc đặt trong nháy.", "Syntax_Missing_Quotes")
    if "unterminated string literal" in error_msg or "EOL while scanning string literal" in error_msg:
        return ("Chưa đóng dấu nháy đơn", "Thiếu dấu nháy đóng.", "Syntax_Missing_Quotes")
    if has_cap_print:
        return ("Viết hoa từ khóa lệnh print", "Lệnh print bắt buộc viết thường.", "Syntax_Print_Capitalized")
    if "was never closed" in error_msg or ("(" in code_str and code_str.count("(") > code_str.count(")")):
        return ("Thiếu dấu đóng ngoặc đơn", "Thiếu ngoặc đơn `)`.", "Syntax_General")

    if error_msg:
        err_low = error_msg.lower()
        m_ln = re.search(r"dòng (\d+)|line (\d+)", error_msg)
        ln_str = f" tại dòng {m_ln.group(1) or m_ln.group(2)}" if m_ln else ""
        
        if "nameerror" in err_low:
            m_name = re.search(r"name '([^']+)' is not defined", error_msg)
            var_n = f"`{m_name.group(1)}`" if m_name else "biến"
            return (f"Sử dụng biến {var_n} chưa được khai báo", f"Biến {var_n} chưa được tạo giá trị trước khi gọi.", "NameError")
        if "invalid literal for int" in err_low:
            return ("Sai kiểu dữ liệu khi ép kiểu", "Dữ liệu nhập chứa số thập phân, cần dùng float().", "Type_Casting_Error")
        if "unsupported operand type" in err_low or "can't multiply sequence" in err_low:
            return ("Chưa ép kiểu dữ liệu số cho input()", "Dữ liệu input() là xâu kí tự, cần bọc hàm số học.", "Type_Casting_Error")
        if "zerodivisionerror" in err_low:
            return ("Thực hiện phép chia cho số 0", "Mẫu số bắt buộc phải khác 0.", "Syntax_General")
        if "indentationerror" in err_low:
            return (f"Sai quy tắc thụt lề{ln_str}", "Thụt lề khối lệnh bắt buộc 4 khoảng trắng.", "IndentationError")
        if "syntaxerror" in err_low or "invalid syntax" in err_low:
            return (f"Sai cú pháp câu lệnh{ln_str}", "Vi phạm quy tắc cú pháp Python.", "SyntaxError")
        
        return (f"Lỗi gián đoạn chương trình{ln_str}", translate_system_error(error_msg), "Syntax_General")

    if has_input_req and "input(" not in code_str:
        return ("Gian lận in cứng kết quả", "Đề bài yêu cầu dùng lệnh `input()` để đọc dữ liệu.", "Anti_Hardcode_Violation")

    if actual_output == "":
        return ("Chưa có lệnh in kết quả", "Chương trình chưa dùng lệnh `print()` để xuất dữ liệu.", "Logic_Missing_Print")

    if passed_tests < total_tests:
        if tests:
            first_exp = str(tests[0].get("expected", "")).strip()
            exp_nums = re.findall(r'[-+]?\d*\.?\d+', first_exp)
            if exp_nums:
                all_found = all(num in actual_output for num in exp_nums)
                if all_found and len(actual_output) > len(first_exp):
                    return ("Lỗi in thừa lời dẫn văn bản", "Thuật toán đúng nhưng máy chấm không cho phép in thêm chữ giải thích.", "Print_Extra_Text")
        
        return ("Kết quả tính toán chưa chính xác", "Chương trình chưa cho ra kết quả chính xác trên các ca kiểm thử.", "Logic_Incorrect_Result")

    return ("Chưa đạt yêu cầu", "Em hãy đối chiếu lại đề bài.", "General")

def generate_scaffolding_guidance(attempt_count, diagnosis, exercise, error_msg=""):
    title, diag_text, diag_tag = diagnosis
    step_guidance = get_step_by_step_scaffolding(exercise, diag_tag, error_msg)
    
    msg = (
        f"🧑‍🏫 **Chẩn đoán Lỗi & Định hướng Socratic (SGK Tin 10):**\n"
        f"- **Vấn đề nhận diện:** {title}.\n"
        f"- **Phân tích:** {purge_hedging(diag_text)}\n\n"
        f"{step_guidance}"
    )
    return purge_hedging(msg)

# ==================== 1. GIAO DIỆN ĐĂNG NHẬP ====================
if not st.session_state.authenticated:
    st.markdown("""
        <div style='background-color: #007bc7; padding: 22px 28px; border-radius: 8px; margin-bottom: 30px; text-align: center;'>
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
is_locked = (user.get("status") in ["Tạm khóa", "locked"] or user.get("strikes", 0) >= 2)

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
        
        if is_locked:
            st.error("🚨 **TÀI KHOẢN ĐANG BỊ TẠM KHÓA DO VI PHẠM KỶ LUẬT ỨNG XỬ.** Vui lòng liên hệ Thầy/Cô bộ môn để mở khóa.")
            st.stop()

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
                st.write("Ngân hàng bài tập theo mức độ nhận thức.")
                if st.button("Xem Bài tập ➡️", key="btn_t_practice", use_container_width=True):
                    st.session_state.nav_page = "📝 Kho Bài Tập Python"
                    st.rerun()
        with c3:
            with st.container(border=True):
                st.markdown("#### 📊 Báo cáo Benchmark")
                st.write("Dữ liệu đánh giá học sinh thời gian thực.")
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
    if is_locked and not is_teacher:
        st.error("🚨 **TÀI KHOẢN ĐÃ BỊ TẠM KHÓA DO VI PHẠM KỶ LUẬT.** Vui lòng liên hệ Thầy/Cô để được mở khóa.")
        st.stop()

    if st.session_state.doing_exercise and st.session_state.current_ex_id:
        curr_ex = next((item for item in REAL_EXERCISES if item["id"] == st.session_state.current_ex_id), REAL_EXERCISES[0])
        tests = curr_ex.get("tests", [])

        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Quay lại danh sách bài", key="btn_back_list"):
                st.session_state.doing_exercise = False
                st.rerun()

        st.markdown(f"### 💻 LÀM BÀI: [{curr_ex['id']}] {curr_ex['title']}")
        st.caption(f"Trọng tâm kiến thức: **{curr_ex['concept']}**")

        col_left, col_right = st.columns([1.25, 1])

        with col_left:
            with st.container(border=True):
                st.markdown(f"#### 🎯 ĐỀ BÀI: {curr_ex['title']} ({curr_ex['difficulty']})")
                st.write(curr_ex['desc'])

            ed_key = f"code_editor_{curr_ex['id']}"
            if ed_key not in st.session_state:
                st.session_state[ed_key] = f"# Viết mã nguồn cho bài {curr_ex['id']}\n"

            student_code = st.text_area(label="Trình soạn thảo mã nguồn Python", value=st.session_state[ed_key], key=ed_key, height=180)

            col_b1, col_b2 = st.columns([1, 1.2])
            
            with col_b1:
                st.markdown('<div class="st-key-btn_submit_main">', unsafe_allow_html=True)
                btn_submit = st.button("Chấm bài", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_b2:
                st.markdown('<div class="st-key-btn_toggle_runner">', unsafe_allow_html=True)
                toggle_label = "Đóng chạy thử" if st.session_state.show_test_runner else "Mở chạy thử"
                if st.button(toggle_label, use_container_width=True):
                    st.session_state.show_test_runner = not st.session_state.show_test_runner
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.show_test_runner:
                in_state_key = f"runner_input_val_{curr_ex['id']}"
                out_state_key = f"runner_output_val_{curr_ex['id']}"
                
                default_test_in = tests[0]["input"] if tests else ""
                if in_state_key not in st.session_state:
                    st.session_state[in_state_key] = default_test_in
                if out_state_key not in st.session_state:
                    st.session_state[out_state_key] = ""

                with st.container(border=True):
                    st.markdown('<div class="custom-green-box"></div>', unsafe_allow_html=True)
                    
                    c_in, c_out = st.columns(2)
                    with c_in:
                        st.text_area(
                            "Input:",
                            key=in_state_key,
                            height=90,
                            placeholder="Nhập dữ liệu vào đây..."
                        )
                    with c_out:
                        st.text_area(
                            "Output:",
                            value=st.session_state[out_state_key],
                            height=90,
                            disabled=True,
                            placeholder="Kết quả xuất ra màn hình..."
                        )
                    
                    c_sp1, c_mid_btn, c_sp2 = st.columns([1.5, 1, 1.5])
                    with c_mid_btn:
                        st.markdown('<div class="st-key-btn_run_action">', unsafe_allow_html=True)
                        if st.button("Chạy thử", use_container_width=True):
                            current_input_feed = st.session_state.get(in_state_key, "").strip()
                            if not current_input_feed and tests:
                                current_input_feed = tests[0].get("input", "")
                                st.session_state[in_state_key] = current_input_feed
                            
                            r_out, r_err = execute_student_script(student_code, current_input_feed)
                            if r_err:
                                st.session_state[out_state_key] = f"Lỗi: {translate_system_error(r_err)}"
                            else:
                                st.session_state[out_state_key] = r_out if r_out else "(Chương trình chạy xong nhưng không xuất gì ra màn hình)"
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

            if btn_submit:
                all_tests = list(tests)
                
                if curr_ex['id'] == "C1_21":
                    rw, rh = round(random.uniform(2.0, 9.0), 1), round(random.uniform(2.0, 9.0), 1)
                    all_tests.append({"input": f"{rw}\n{rh}", "expected": str(round(rw * rh, 2))})
                elif curr_ex['id'] == "C1_31":
                    rsec = random.randint(100, 86400)
                    all_tests.append({"input": str(rsec), "expected": f"{rsec // 3600} giờ {(rsec % 3600) // 60} phút {rsec % 60} giây"})

                passed_tests = 0
                test_logs = []
                first_error = ""
                first_actual = ""
                total_t = len(all_tests)

                for idx, t in enumerate(all_tests):
                    inp_data = t.get("input", "")
                    actual_out, err_msg = execute_student_script(student_code, inp_data)

                    if err_msg:
                        if not first_error:
                            first_error = err_msg
                        test_logs.append(f"Ca kiểm thử #{idx + 1}: ❌ Chưa chính xác")
                    else:
                        exp_out = str(t.get("expected", "")).strip()
                        if is_output_semantically_correct(actual_out, exp_out):
                            passed_tests += 1
                            test_logs.append(f"Ca kiểm thử #{idx + 1}: ✔️ Chính xác")
                        else:
                            if not first_actual:
                                first_actual = actual_out
                            test_logs.append(f"Ca kiểm thử #{idx + 1}: ❌ Chưa chính xác")

                score = round((passed_tests / total_t) * 10.0, 1) if total_t > 0 else 0.0

                diag_title, diag_desc, diag_tag = diagnose_student_misconception(
                    student_code, first_error, first_actual, curr_ex, passed_tests, total_t
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
                    st.success(f"🎉 Hoàn thành xuất sắc! - Đạt chuẩn SGK Tin 10: {score}/10 Điểm")
                    guidance = "🎉 **Chúc mừng em!** Chương trình chạy chính xác hoàn toàn theo đúng yêu cầu đề bài."
                else:
                    st.warning(f"⚠️ Chưa đạt yêu cầu - {passed_tests}/{total_t} Ca kiểm thử: {score}/10 Điểm")
                    guidance = generate_scaffolding_guidance(attempt_count, (diag_title, diag_desc, diag_tag), curr_ex, first_error)

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

            with st.container(height=480):
                if not st.session_state.messages:
                    st.caption("Thầy/Cô Trợ lý AI sẵn sàng trò chuyện, giải đáp mọi thắc mắc và hướng dẫn từng bước.")
                for m in st.session_state.messages:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])

            if user_prompt := st.chat_input("Nhập câu hỏi, thắc mắc hoặc trò chuyện với AI..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                if check_profanity(user_prompt):
                    if not is_teacher:
                        add_strike(user.get('account_id'))
                        st.session_state.user["strikes"] = st.session_state.user.get("strikes", 0) + 1
                        st.session_state.user["status"] = "Tạm khóa"
                    st.error("🚨 **TÀI KHOẢN ĐÃ BỊ KHÓA NGAY LẬP TỨC!** Em đã vi phạm quy chuẩn văn hóa ứng xử.")
                    st.rerun()
                else:
                    ai_ans = generate_conversational_ai_response(user_prompt, curr_ex, student_code)
                
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
                            clean_inp = inp.replace('\n', ' ; ')
                            st.caption(f"- **Test #{idx + 1}:** Input = `{clean_inp}` ➔ Output = `{t['expected']}`")
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
                st.write(f"**Số lần vi phạm kỷ luật:** `{user.get('strikes', 0)}/2`")
                
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