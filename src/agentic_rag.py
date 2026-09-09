import os
import re
import ast
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from src.curriculum import SGK_CURRICULUM
from src.utils.profanity_filter import check_profanity

load_dotenv()

# Nạp an toàn mô hình Gemini (Không gây cảnh báo Pylance)
gemini_model = None
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_KEY and not GOOGLE_KEY.startswith("AIzaSy_dien_ma"):
    try:
        import importlib
        genai_lib = importlib.import_module("langchain_google_genai")
        ChatGoogle = getattr(genai_lib, "ChatGoogleGenerativeAI", None)
        if ChatGoogle:
            gemini_model = ChatGoogle(model="gemini-1.5-flash", google_api_key=GOOGLE_KEY, temperature=0.2)
    except Exception:
        gemini_model = None

def is_python_code(text: str) -> bool:
    s = text.strip()
    patterns = [
        r"\bdef\s+\w+\s*\(", r"\bprint\s*\(", r"\binput\s*\(",
        r"\bfor\s+\w+\s+in\b", r"\bwhile\b.+:", r"\bif\b.+:",
        r"\belif\b.+:", r"\belse\s*:", r"\bimport\b", r"\breturn\b"
    ]
    if any(re.search(p, s) for p in patterns):
        return True
    if "\n" in s and any(op in s for op in ["=", "+=", "==", "!="]):
        return True
    return False

def analyze_student_code(code_text: str) -> tuple[bool, str]:
    c = code_text.strip()
    if "input()" in c and not any(f in c for f in ["int(input", "float(input"]):
        return True, "💡 **Lưu ý kiểu dữ liệu (Bài 18 SGK):** Hàm `input()` trả về kiểu chuỗi (`str`). Khi dùng `+`, Python sẽ nối chuỗi thay vì tính tổng số học. Em cần dùng `int()` hoặc `float()` để ép kiểu sang số nhé!"
    if re.search(r'\bif\b\s+[^=><!]+=[^=]', c):
        return True, "💡 **Lỗi phép toán so sánh (Bài 19 SGK):** Dấu một bằng `=` là phép gán. Để so sánh bằng nhau trong mệnh đề `if`, toán tử đúng trong Python là `==`."
    for line in c.split("\n"):
        ls = line.strip()
        for kw in ["if", "elif", "else", "for", "while", "def"]:
            if ls.startswith(kw) and not ls.endswith(":"):
                return True, f"💡 **Lỗi cú pháp khối lệnh:** Cuối câu lệnh `{kw}` trong Python bắt buộc phải có dấu hai chấm `:`."
    if c.count("(") != c.count(")"):
        return True, "💡 **Lỗi cú pháp:** Số lượng dấu mở ngoặc `(` và đóng ngoặc `)` chưa khớp nhau."
    try:
        ast.parse(c)
    except SyntaxError as se:
        if "indent" in str(se).lower():
            return True, "💡 **Lỗi thụt lề (IndentationError):** Các lệnh bên trong khối lệnh bắt buộc thụt lề đồng nhất 4 khoảng trắng."
        return True, "💡 **Lỗi cú pháp (SyntaxError):** Đoạn mã chưa đúng ngữ pháp Python. Em hãy rà soát lại cấu trúc câu lệnh theo SGK."
    return False, "✅ **Cú pháp chính xác!** Đoạn mã không có lỗi cú pháp. Em hãy chạy thử các trường hợp dữ liệu kiểm thử (test cases) nhé!"

def self_correct_anti_leak(response: str) -> str:
    blocks = re.findall(r"```(?:python)?(.*?)```", response, re.DOTALL)
    for b in blocks:
        lines = [ln for ln in b.strip().split("\n") if ln.strip()]
        if len(lines) >= 3:
            return """🎯 **Gợi ý phương pháp tư duy từng bước (Socratic):**
1. **Bước 1 (Nhập dữ liệu):** Nhập các biến từ bàn phím và ép kiểu phù hợp (`int()` hoặc `float()`).
2. **Bước 2 (Giải thuật):** Dùng câu lệnh điều kiện `if-else` hoặc vòng lặp `for/while` để giải quyết yêu cầu bài toán.
3. **Bước 3 (Xuất kết quả):** Dùng lệnh `print()` để in đáp số.

*Em hãy viết thử 1-2 câu lệnh đầu tiên và gửi lên để thầy/cô cùng em sửa nhé!*"""
    return response

def agentic_tutor_process(user_message: str, current_ch: str, current_ex: dict, strikes: int, wrong_attempts: int):
    msg_cleaned = user_message.strip()
    msg_lower = msg_cleaned.lower()

    # Track 1: Giám sát Liêm chính & Nề nếp
    is_toxic, toxic_word = check_profanity(msg_cleaned)
    begging_words = ["cho xin code", "giải hộ", "full code", "chép code", "làm hộ", "cho đáp án luôn", "viết hộ code", "giải bài này giúp"]
    is_begging = any(bw in msg_lower for bw in begging_words)

    if is_toxic or is_begging:
        new_strikes = strikes + 1
        reason = f"ngôn từ không chuẩn mực ('{toxic_word}')" if is_toxic else "yêu cầu cung cấp toàn bộ code giải sẵn"
        if new_strikes >= 3:
            return {
                "response": "🚫 [TÀI KHOẢN ĐÃ BỊ ĐÌNH CHỈ] Em đã vi phạm quy chế học vụ 3 lần. Hệ thống đã khóa tài khoản theo Điều 5. Vui lòng liên hệ trực tiếp Giáo viên bộ môn.",
                "strikes": new_strikes, "wrong_attempts": wrong_attempts, "is_locked": True, "force_theory": False
            }
        return {
            "response": f"⚠️ [CẢNH BÁO NỀ NẾP LẦN {new_strikes}/3] Em đang vi phạm do {reason}. Thầy/cô chỉ hướng dẫn phương pháp tư duy, tuyệt đối không giải bài hộ!",
            "strikes": new_strikes, "wrong_attempts": wrong_attempts, "is_locked": False, "force_theory": False
        }

    # Track 2: Soát lỗi code thực tế
    if is_python_code(msg_cleaned):
        is_err, feedback = analyze_student_code(msg_cleaned)
        new_wrong = wrong_attempts + 1 if is_err else max(0, wrong_attempts - 1)
        if new_wrong >= 3:
            return {
                "response": "📢 [CẢNH BÁO SỚM EWS] Em đã thử sai liên tiếp 3 lần. Hệ thống tạm khóa nộp code để em củng cố lại lý thuyết nền tảng trong SGK.",
                "strikes": strikes, "wrong_attempts": new_wrong, "is_locked": False, "force_theory": True
            }
        return {"response": feedback, "strikes": strikes, "wrong_attempts": new_wrong, "is_locked": False, "force_theory": False}

    # Track 3: Gợi mở Socratic & RAG SGK
    ch_info = SGK_CURRICULUM.get(current_ch, SGK_CURRICULUM["c1"])
    if gemini_model:
        prompt = f"""Bạn là Giáo viên Tin học 10 (Chương trình GDPT 2018).
Chủ đề: {ch_info['name']}
Bài tập: {current_ex.get('title', '')}
Yêu cầu: {current_ex.get('problem', '')}

LÝ THUYẾT SGK TIN HỌC 10 (BGD&ĐT):
{ch_info.get('content', '')}

NGUYÊN TẮC:
1. TUYỆT ĐỐI KHÔNG cấp full code giải bài hoàn chỉnh.
2. Dùng câu hỏi gợi mở Socratic từng bước để học sinh tự làm."""
        try:
            raw = gemini_model.invoke([SystemMessage(content=prompt), AIMessage(content=msg_cleaned)]).content
            final = self_correct_anti_leak(raw)
            return {"response": final, "strikes": strikes, "wrong_attempts": wrong_attempts, "is_locked": False, "force_theory": False}
        except Exception:
            pass

    fallback = f"""🎯 **Gợi ý từ SGK Tin học 10 ({current_ex.get('title', 'Bài tập')}):**
1. Xác định dữ liệu đầu vào (Input) và kết quả cần in ra (Output).
2. Vận dụng kiến thức trong {ch_info['name']}.
3. Em hãy viết thử câu lệnh đầu tiên và gửi lên để cùng kiểm tra nhé!"""
    return {"response": fallback, "strikes": strikes, "wrong_attempts": wrong_attempts, "is_locked": False, "force_theory": False}

# Bí danh tương thích với mọi cách gọi hàm
process_agentic_workflow = agentic_tutor_process