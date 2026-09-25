from dotenv import load_dotenv
load_dotenv()
import os
import io
import sys
import re
import random
import builtins
import sqlite3
import streamlit as st
import pandas as pd
import google.generativeai as genai

from src.security import (
    check_profanity,
    record_violation,
    get_user_status,
    unlock_account,
    get_all_locked_accounts
)
from src.sgk_data import SGK_CURRICULUM
from src.exercises import REAL_EXERCISES, get_all_exercises_standardized

exercises = get_all_exercises_standardized()
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

# ==================== CƠ CHẾ AI SOCRATIC CHUYÊN GIA (GEMINI API) ====================
def generate_socratic_ai_response(
    prompt: str,
    curr_ex: dict,
    student_code: str,
    chat_history: list = None,
    runtime_err: str = ""
) -> str:
    """Gọi trực tiếp Google Gemini API để giải đáp thông minh, trực diện, không né tránh."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            api_key = None

    ex_title = curr_ex.get('title', 'Bài tập')
    ex_desc = curr_ex.get('desc', '')
    ex_concept = curr_ex.get('concept', '')

    if not api_key:
        return (
            f"Thầy/Cô đang đồng hành cùng em ở bài **'{ex_title}'**.\n\n"
            f"🎯 **Trọng tâm bài học:** {ex_concept}\n\n"
            f"*(Hệ thống chưa tìm thấy `GEMINI_API_KEY` trong file .env hoặc secrets. "
            f"Em hãy kiểm tra khóa API để kích hoạt toàn bộ trí thông minh của AI nhé!)*"
        )

    try:
        genai.configure(api_key=api_key)
        system_instruction = (
            "Bạn là Thầy/Cô Trợ lý Socratic AI chuyên gia giảng dạy Tin học môn Python "
            "lớp 10 theo chương trình GDPT 2018 (Bộ sách Kết nối tri thức với cuộc sống).\n"
            "Bạn sở hữu trí tuệ uyên bác, giao tiếp tự nhiên, thấu hiểu tâm lý học sinh, "
            "đối đáp thông minh và trực diện như ChatGPT/Claude.\n\n"
            "NGUYÊN TẮC GIẢI ĐÁP CỐT LÕI:\n"
            "1. TRẢ LỜI ĐÚNG TRỌNG TÂM - KHÔNG NÉ TRÁNH:\n"
            "   - Khi học sinh hỏi bất kỳ điều gì (về thuật toán, cú pháp, khái niệm biến, "
            "hàm, vòng lặp, giải thích lỗi, kiến thức mở rộng hay đời sống), hãy trả lời "
            "TRỰC DIỆN, THÔNG MINH, giải thích bản chất cặn kẽ và chuẩn xác.\n"
            "   - Tuyệt đối KHÔNG hỏi vặn ngược lặp lại một cách né tránh sáo rỗng. Hãy cung "
            "cấp tri thức trước, hướng dẫn tư duy logic rõ ràng.\n"
            "2. BẮT ĐÚNG BỆNH VÀ PHÂN TÍCH RÕ NGUYÊN NHÂN LỖI:\n"
            "   - Quan sát mã nguồn học sinh đang viết và lỗi thực thi (nếu có).\n"
            "   - Chỉ rõ chính xác dòng nào sai và bản chất kỹ thuật (ví dụ: hàm input() "
            "trả về chuỗi str nên cần ép kiểu int; sau if cần dấu hai chấm : và thụt lề 4 dấu cách...).\n"
            "   - Hướng dẫn các bước logic để học sinh tự chỉnh sửa mã.\n"
            "3. NGUYÊN TẮC ZERO FULL-CODE LEAK (KHÔNG GIẢI HỘ CẢ BÀI TẬP):\n"
            "   - Tuyệt đối không xuất toàn bộ đoạn code giải hoàn chỉnh của bài tập đang làm "
            "để học sinh chỉ việc copy-paste nộp bài.\n"
            "   - BẠN ĐƯỢC PHÉP: Đưa ra ví dụ code minh họa độc lập (1-3 dòng) của bài toán "
            "khác để học sinh hiểu cú pháp, hoặc đưa khung code điền khuyết (dùng dấu ...) "
            "để học sinh tự làm.\n"
            "   - Nếu học sinh xin trực tiếp code đáp án: Từ chối hóm hỉnh, khích lệ và chỉ "
            "rõ các bước thuật toán I-P-O để học sinh tự tay lập trình."
        )

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )

        gemini_hist = []
        if chat_history:
            for m in chat_history[:-1]:
                role = "user" if m.get("role") == "user" else "model"
                cnt = str(m.get("content", "")).strip()
                if cnt:
                    gemini_hist.append({"role": role, "parts": [cnt]})

        code_preview = student_code.strip() if student_code.strip() else "# Khung soạn thảo đang trống"
        err_context = runtime_err.strip() if runtime_err.strip() else "Không có lỗi runtime"

        full_prompt = (
            f"[THÔNG TIN BÀI TẬP VÀ MÃ NGUỒN HIỆN TẠI]\n"
            f"- Tên bài tập: {ex_title}\n"
            f"- Yêu cầu đề bài: {ex_desc}\n"
            f"- Trọng tâm kiến thức: {ex_concept}\n"
            f"- Mã nguồn học sinh đang viết:\n```python\n{code_preview}\n```\n"
            f"- Trạng thái kiểm thử / Lỗi runtime: {err_context}\n"
            f"--------------------------------------------------\n"
            f"HỌC SINH HỎI: \"{prompt}\"\n\n"
            f"(Yêu cầu: Trả lời thẳng vào trọng tâm câu hỏi của học sinh, giải thích cặn kẽ, "
            f"chính xác và nhiệt tình. Nếu code sai hãy chỉ đúng vị trí và nguyên nhân. "
            f"Hướng dẫn tư duy logic chi tiết nhưng không đưa toàn bộ code giải hoàn chỉnh.)"
        )

        chat = model.start_chat(history=gemini_hist)
        res = chat.send_message(full_prompt)
        raw_reply = res.text.strip()

        # Chốt chặn Guardrail: Chặn khối mã giải hoàn chỉnh dài trên 8 dòng
        def check_leak(match):
            body = match.group(1).strip()
            lines = [l for l in body.splitlines() if l.strip()]
            if len(lines) >= 8 and ("def " in body or "print" in body):
                return "\n*(Thầy/Cô đã hướng dẫn thuật toán chi tiết ở trên, em hãy tự ráp các câu lệnh vào khung bên trái nhé!)*\n"
            return match.group(0)

        filtered = re.sub(r"```(?:python)?\s*([\s\S]*?)```", check_leak, raw_reply)
        return filtered.strip()

    except Exception:
        return (
            f"Thầy/Cô đang đồng hành cùng em ở bài **'{ex_title}'**. "
            f"Trọng tâm của bài này là **{ex_concept}**. "
            f"Em hãy bấm nút '▶️ Chạy thử' ở bên trái để chúng ta cùng xem kết quả nhé!"
        )

# ==================== CÁC HÀM XỬ LÝ LỖI & THỰC THI SANDBOX ====================
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

# ĐỒNG BỘ TRẠNG THÁI KHÓA VĨNH VIỄN TỪ Ổ CỨNG (FILE JSON & CSDL)
student_account_id = user.get("account_id") or user.get("email")
sec_status = get_user_status(student_account_id)
is_locked = (
    user.get("status") in ["Tạm khóa", "locked"]
    or user.get("strikes", 0) >= 3
    or sec_status.get("locked", False)
)

# CHỐT CHẶN CỨNG BẢO VỆ: NẾU ĐÃ BỊ KHÓA 3 LẦN THÌ DÙ CÓ F5 HAY ĐĂNG NHẬP LẠI VẪN BỊ CHẶN ĐỨNG
if is_locked and not is_teacher:
    st.markdown("""
        <div style='background-color: #c9302c; padding: 16px; border-radius: 8px; margin-bottom: 20px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>🚨 TÀI KHOẢN ĐÃ BỊ KHÓA VĨNH VIỄN DO VI PHẠM KỶ LUẬT</h3>
        </div>
    """, unsafe_allow_html=True)
    st.error(f"Học sinh **{user['full_name']}** (`{student_account_id}`) đã vi phạm chuẩn mực phát ngôn học đường 3 lần liên tiếp.")
    st.info("Toàn bộ quyền làm bài, luyện tập và trao đổi với Trợ lý AI đã bị đình chỉ. Em vui lòng gặp trực tiếp Thầy/Cô bộ môn để giải trình và xem xét mở khóa.")

    if st.button("🚪 Đăng Xuất Khỏi Hệ Thống", type="secondary"):
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.nav_page = "🏠 Trang chủ"
        st.session_state.doing_exercise = False
        st.session_state.messages = []
        st.rerun()
    st.stop()

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
    st.markdown("## 📖 CỐT LÕI KIẾN THỨC SGK TIN HỌC 10")

    lesson_keys = list(SGK_CURRICULUM.keys())
    lesson_titles = [SGK_CURRICULUM[k]["name"] for k in lesson_keys]

    selected_index = st.selectbox(
        "Chọn bài học:",
        range(len(lesson_keys)),
        format_func=lambda i: lesson_titles[i]
    )

    chosen_lesson = SGK_CURRICULUM[lesson_keys[selected_index]]

    with st.container():
        st.markdown(f"### 📘 {chosen_lesson['name']}")
        if "chapter" in chosen_lesson:
            st.caption(f"📁 {chosen_lesson['chapter']}")
        st.markdown("---")
        st.markdown(chosen_lesson["theory"])

# ----------------- TAB 3: KHO BÀI TẬP PYTHON -----------------
elif st.session_state.nav_page == "📝 Kho Bài Tập Python":
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

            in_state_key = f"runner_input_val_{curr_ex['id']}"
            out_state_key = f"runner_output_val_{curr_ex['id']}"

            default_test_in = tests[0]["input"] if tests else ""
            if in_state_key not in st.session_state:
                st.session_state[in_state_key] = default_test_in
            if out_state_key not in st.session_state:
                st.session_state[out_state_key] = ""

            if st.session_state.show_test_runner:
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

            # XỬ LÝ CHAT THÔNG MINH & QUY TẮC KỶ LUẬT 3-STRIKE CHỐNG F5
            if user_prompt := st.chat_input("Nhập câu hỏi, thắc mắc hoặc trò chuyện với AI..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                # 1. KIỂM DUYỆT TỪ NGỮ THÔ TỤC
                if check_profanity(user_prompt):
                    if not is_teacher:
                        # Ghi nhận vi phạm vào cả CSDL SQLite và tệp JSON bền vững
                        add_strike(user.get('account_id'))
                        strikes_cnt, is_now_locked = record_violation(student_account_id, user_prompt)
                        st.session_state.user["strikes"] = strikes_cnt

                        if strikes_cnt == 1:
                            ai_ans = (
                                "⚠️ **CẢNH BÁO LẦN 1/3:** Em vừa sử dụng từ ngữ chưa phù hợp chuẩn mực học đường. "
                                "Em hãy giữ lời nói văn minh để cùng học tập tiến bộ nhé!"
                            )
                        elif strikes_cnt == 2:
                            ai_ans = (
                                "🚨 **CẢNH BÁO LẦN 2/3:** Em đã vi phạm phát ngôn lần thứ 2! "
                                "Nếu vi phạm thêm **1 lần nữa**, tài khoản sẽ bị **KHÓA VĨNH VIỄN** "
                            )
                        else:
                            st.session_state.user["status"] = "Tạm khóa"
                            ai_ans = (
                                "🔒 **TÀI KHOẢN ĐÃ BỊ KHÓA:** Em đã vi phạm quy định ngôn từ 3 lần liên tiếp. "
                                "Quyền truy cập hệ thống của em đã bị đình chỉ. Vui lòng liên hệ Thầy/Cô để giải trình."
                            )
                            st.session_state.messages.append({"role": "assistant", "content": ai_ans})
                            st.rerun()
                    else:
                        ai_ans = "⚠️ Cảnh báo: Giáo viên không nên sử dụng từ ngữ này trong môi trường sư phạm."
                else:
                    # 2. GIA SƯ AI THÔNG MINH TRỰC TIẾP TỪ GEMINI
                    with st.spinner("Thầy/Cô AI đang xem xét bài và giải đáp..."):
                        ai_ans = generate_socratic_ai_response(
                            prompt=user_prompt,
                            curr_ex=curr_ex,
                            student_code=student_code,
                            chat_history=st.session_state.messages,
                            runtime_err=st.session_state.get(out_state_key, "")
                        )

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
                                unlock_account(s['account_id'])
                                st.success(f"Đã mở khóa thành công cho {s['full_name']}!")
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