import os
import re
import ast
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from src.curriculum import SGK_CURRICULUM
from src.utils.profanity_filter import check_profanity

load_dotenv()

# Khởi tạo mô hình Gemini an toàn (tránh cảnh báo Pylance)
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
gemini_model = None
if GOOGLE_KEY and not GOOGLE_KEY.startswith("AIzaSy_dien_ma"):
    try:
        import importlib
        genai_mod = importlib.import_module("langchain_google_genai")
        ChatGoogle = getattr(genai_mod, "ChatGoogleGenerativeAI", None)
        if ChatGoogle:
            gemini_model = ChatGoogle(model="gemini-1.5-flash", google_api_key=GOOGLE_KEY, temperature=0.2)
    except Exception:
        gemini_model = None

# Trích xuất dữ liệu trực tiếp từ file PDF SGK trong thư mục data/
PDF_CACHE = []
def search_pdf_sgk(query: str, top_k: int = 2) -> str:
    global PDF_CACHE
    pdf_path = Path(__file__).resolve().parent.parent / "data" / "sgk_tin10.pdf"
    if not pdf_path.exists():
        return ""
    if not PDF_CACHE:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_path))
            for p_idx, p in enumerate(reader.pages):
                t = p.extract_text()
                if t and t.strip():
                    PDF_CACHE.append({"page": p_idx + 1, "text": t.strip()})
        except Exception:
            return ""
            
    q_words = [w for w in query.lower().split() if len(w) > 2]
    matched = []
    for item in PDF_CACHE:
        score = sum(1 for w in q_words if w in item["text"].lower())
        if score > 0:
            matched.append((score, item))
    matched.sort(key=lambda x: x[0], reverse=True)
    if matched:
        return "\n\n".join([f"📖 [Trích từ Trang {m[1]['page']} SGK Tin 10]:\n{m[1]['text'][:600]}" for m in matched[:top_k]])
    return ""

REGULATION_KNOWLEDGE = {
    "tre": "📋 Căn cứ Điều 1 Quy chế: Vào lớp trễ dưới 15 phút phải báo cáo trực tiếp GV bộ môn. Vắng quá 20% số tiết không phép sẽ bị cấm thi.",
    "vang": "📋 Căn cứ Điều 1 Quy chế: Nghỉ học có phép phải nộp đơn trong 48h và hoàn thành bài bù trong 7 ngày.",
    "muon": "📋 Căn cứ Điều 2 Quy chế: Nộp trễ < 24h trừ 20% điểm; 24h - 48h trừ 50%; quá 48h nhận điểm 0.",
    "gian_lan": "📋 Căn cứ Điều 3 Quy chế: Cấm sao chép code hoặc xin AI giải hộ. Vi phạm lần 1 nhận điểm 0; lần 2 hạ bậc rèn luyện.",
    "ews": "📋 Căn cứ Điều 4 Quy chế: Thử sai 3 lần liên tiếp kích hoạt Cảnh báo sớm (EWS) để tạm dừng nộp bài và ôn tập lại lý thuyết SGK.",
    "strike": "📋 Căn cứ Điều 5 Quy chế: Vi phạm quy chuẩn ngôn từ hoặc liêm chính 3 lần sẽ bị khóa tài khoản vĩnh viễn."
}

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

def analyze_code_static(code_text: str) -> tuple[bool, str]:
    c = code_text.strip()
    if "input()" in c and not any(f in c for f in ["int(input", "float(input"]):
        return True, "💡 **Lưu ý kiểu dữ liệu (Bài 18 SGK):** Hàm `input()` luôn trả về kiểu xâu (`str`). Khi cộng hai xâu `'5' + '6'`, kết quả là `'56'` chứ không thành `11`. Em cần dùng hàm `int()` hoặc `float()` để ép kiểu sang số nhé!"
    if re.search(r'\bif\b\s+[^=><!]+=[^=]', c):
        return True, "💡 **Lỗi phép toán so sánh (Bài 19 SGK):** Dấu một bằng `=` là phép gán. Để so sánh bằng nhau trong mệnh đề `if`, toán tử đúng là `==`."
    for line in c.split("\n"):
        ls = line.strip()
        for kw in ["if", "elif", "else", "for", "while", "def"]:
            if ls.startswith(kw) and not ls.endswith(":"):
                return True, f"💡 **Lỗi cú pháp:** Cuối câu lệnh `{kw}` bắt buộc phải có dấu hai chấm `:` để mở khối lệnh bên dưới."
    if c.count("(") != c.count(")"):
        return True, "💡 **Lỗi cú pháp:** Số lượng dấu mở ngoặc `(` và đóng ngoặc `)` chưa khớp nhau."
    try:
        ast.parse(c)
    except SyntaxError as se:
        if "indent" in str(se).lower():
            return True, "💡 **Lỗi thụt lề (IndentationError):** Các câu lệnh bên trong khối `if`, `for`, `while`, `def` bắt buộc phải thụt lề đồng nhất 4 khoảng trắng."
        return True, "💡 **Lỗi cú pháp (SyntaxError):** Đoạn mã chưa đúng ngữ pháp Python. Em hãy rà soát lại cấu trúc câu lệnh theo SGK."
    return False, "✅ **Cú pháp chính xác!** Đoạn mã không có lỗi cú pháp. Em hãy chạy thử các trường hợp dữ liệu (test cases) để kiểm tra logic giải thuật nhé!"

def reflect_and_filter_code_leak(response: str) -> str:
    """Tự phản tư và chặn triệt để hành vi cấp full code (Anti-Code-Leak)"""
    blocks = re.findall(r"```(?:python)?(.*?)```", response, re.DOTALL)
    for b in blocks:
        lines = [ln for ln in b.strip().split("\n") if ln.strip()]
        if len(lines) >= 3:
            return """🎯 **Gợi ý phương pháp tư duy từng bước (Socratic):**
1. **Bước 1 (Nhập dữ liệu):** Nhập các biến từ bàn phím và ép kiểu phù hợp (`int()` hoặc `float()`).
2. **Bước 2 (Giải thuật):** Áp dụng câu lệnh điều kiện `if-else` hoặc vòng lặp `for/while` để xử lý bài toán.
3. **Bước 3 (Xuất kết quả):** Dùng lệnh `print()` để in đáp số.

*Em hãy viết thử 1-2 câu lệnh đầu tiên và gửi lên đây để thầy/cô cùng em sửa nhé!*"""
    return response

def process_agentic_workflow(user_msg: str, ch_key: str, exercise_info: dict, strikes: int, wrong_count: int):
    u_msg = user_msg.strip()
    u_lower = u_msg.lower()

    # Track 1: Giám sát Liêm chính & Nề nếp
    is_profane, toxic_w = check_profanity(u_msg)
    cheating_kw = ["cho xin code", "giải hộ", "full code", "chép code", "làm hộ", "cho đáp án luôn", "viết hộ code", "giải bài này giúp"]
    is_begging = any(kw in u_lower for kw in cheating_kw)

    if is_profane or is_begging:
        new_s = strikes + 1
        reason = f"ngôn từ chưa chuẩn mực ('{toxic_w}')" if is_profane else "yêu cầu cung cấp toàn bộ code giải sẵn"
        if new_s >= 3:
            return {
                "reply": "🚫 [TÀI KHOẢN ĐÃ BỊ ĐÌNH CHỈ] Em đã vi phạm quy chế học vụ 3 lần. Hệ thống đã khóa tài khoản theo Điều 5. Vui lòng liên hệ Giáo viên bộ môn.",
                "strikes": new_s, "wrong": wrong_count, "is_locked": True, "force_theory": False
            }
        return {
            "reply": f"⚠️ [CẢNH BÁO NỀ NẾP LẦN {new_s}/3] Em đang vi phạm do {reason}. Thầy/cô chỉ hướng dẫn phương pháp tư duy, tuyệt đối không giải bài hộ!",
            "strikes": new_s, "wrong": wrong_count, "is_locked": False, "force_theory": False
        }

    # Track 2: RAG Quy chế học vụ
    reg_words = ["quy chế", "nộp muộn", "trừ điểm", "nghỉ học", "vắng", "deadline", "điểm 0", "quy định", "cấm thi", "đến trễ", "vào trễ", "trễ", "xin phép"]
    if any(rw in u_lower for rw in reg_words) and not is_python_code(u_msg):
        for k, v in REGULATION_KNOWLEDGE.items():
            if k in u_lower or (k == "tre" and any(w in u_lower for w in ["trễ", "muộn"])):
                return {"reply": v, "strikes": strikes, "wrong": wrong_count, "is_locked": False, "force_theory": False}
        return {"reply": REGULATION_KNOWLEDGE["strike"], "strikes": strikes, "wrong": wrong_count, "is_locked": False, "force_theory": False}

    # Track 3: Soát lỗi Code thực tế (AST Linter)
    if is_python_code(u_msg):
        is_err, feedback = analyze_code_static(u_msg)
        new_w = wrong_count + 1 if is_err else max(0, wrong_count - 1)
        if new_w >= 3:
            return {
                "reply": "📢 [CẢNH BÁO SỚM EWS] Em đã thử sai liên tiếp 3 lần. Hệ thống tạm khóa nộp code để em ôn tập lại lý thuyết nền tảng trong SGK.",
                "strikes": strikes, "wrong": new_w, "is_locked": False, "force_theory": True
            }
        return {"reply": feedback, "strikes": strikes, "wrong": new_w, "is_locked": False, "force_theory": False}

    # Track 4: RAG từ File PDF SGK & Socratic Guidance
    ch_data = SGK_CURRICULUM.get(ch_key, SGK_CURRICULUM.get("c1", {}))
    pdf_context = search_pdf_sgk(f"{u_msg} {exercise_info.get('title', '')}")
    if not pdf_context:
        pdf_context = ch_data.get('content', '')

    if gemini_model:
        prompt = f"""Bạn là Giáo viên Tin học 10 chuẩn mực sư phạm (GDPT 2018).
Chủ đề: {ch_data.get('name', '')}
Bài tập đang làm: {exercise_info.get('title', '')}
Mô tả yêu cầu: {exercise_info.get('problem', '')}

DỮ LIỆU NGUYÊN BẢN TỪ SGK TIN HỌC 10 (BGD&ĐT):
{pdf_context}

NGUYÊN TẮC:
1. TUYỆT ĐỐI KHÔNG viết toàn bộ code hoàn chỉnh.
2. Dẫn chứng lý thuyết SGK và gợi mở Socratic từng bước để học sinh tự làm."""
        try:
            raw = gemini_model.invoke([SystemMessage(content=prompt), AIMessage(content=u_msg)]).content
            final = reflect_and_filter_code_leak(raw)
            return {"reply": final, "strikes": strikes, "wrong": wrong_count, "is_locked": False, "force_theory": False}
        except Exception:
            pass

    fallback = f"""🎯 **Gợi ý từ SGK Tin học 10 ({exercise_info.get('title', 'Bài tập')}):**
1. Đọc kỹ đề bài để xác định biến đầu vào (Input) và đầu ra (Output).
2. Áp dụng cấu trúc trong {ch_data.get('name', 'bài học')}.
3. Em hãy viết thử câu lệnh đầu tiên và gửi lên để kiểm tra nhé!"""
    return {"reply": fallback, "strikes": strikes, "wrong": wrong_count, "is_locked": False, "force_theory": False}

# Bí danh tương thích
tutor_agent_app = process_agentic_workflow