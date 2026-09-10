import os
import re
import ast
import streamlit as st
import google.generativeai as genai

# Tự động kết nối hàm phạt kỷ luật trong database
try:
    from src.db import add_user_strike
except Exception:
    def add_user_strike(account_id: str):
        return 1, False

SYSTEM_PROMPT = (
    "Bạn là 'Trợ lý Sư phạm AI Tin học 10' thông minh và nghiêm khắc của EduCoder 10 (Chương trình GDPT 2018).\n\n"
    "NGUYÊN TẮC PHẢN HỒI:\n"
    "1. VẠCH RÕ CHỖ SAI: Phân tích trực diện mã nguồn của học sinh, chỉ ra dòng thiếu, lỗi cú pháp hoặc sai thuật toán.\n"
    "2. HƯỚNG DẪN TỪNG BƯỚC (SOCRATIC): Giải thích nguyên lý tại sao máy tính không chạy được và gợi ý câu lệnh mẫu chuẩn SGK.\n"
    "3. XƯNG HÔ: Luôn xưng 'Thầy/Cô' và gọi 'em'."
)

BAD_WORDS = [
    "cặc", "cac", "lồn", "lon", "buồi", "buoi", "địt", "dit", "đụ", "du",
    "đéo", "deo", "đm", "dcm", "vcl", "vl", "cl", "mẹ mày", "me may",
    "mẹ m", "chó", "óc chó", "ngu", "dốt", "cút"
]

def check_inappropriate_language(text: str) -> bool:
    """Nhận diện chính xác từ ngữ thô tục, chửi thề."""
    low = " " + text.lower().strip() + " "
    low = re.sub(r"[._\-\s+]", " ", low)
    for bw in BAD_WORDS:
        if f" {bw} " in low or bw in low:
            return True
    return False

def analyze_curriculum_exercise(code: str, title: str, problem: str, judge_details: str) -> str:
    """
    Bộ chuyên gia sư phạm phân tích mã nguồn cho toàn bộ 5 chủ đề (C1 đến C5):
    - C1: Nhập/xuất, số học, ép kiểu int/float
    - C2: Rẽ nhánh if/else
    - C3: Vòng lặp for/while
    - C4: Xử lý chuỗi (str)
    - C5: Danh sách (list) và hàm (def)
    """
    code_strip = code.strip()
    full_info = (title + " " + problem).lower()

    # 1. Chưa viết mã nguồn
    if not code_strip or code_strip.startswith("# Viết mã nguồn"):
        return (
            f"💡 **Thầy/Cô hướng dẫn em giải bài {title}:**\n\n"
            f"- **Yêu cầu đề bài:** {problem}\n"
            "- **Các bước làm:**\n"
            "  1. Nhập dữ liệu đầu vào bằng `input()`, nhớ ép kiểu `int()` hoặc `float()` nếu là số.\n"
            "  2. Thiết lập công thức hoặc vòng lặp xử lý thuật toán.\n"
            "  3. In kết quả ra màn hình bằng hàm `print()` theo đúng định dạng đề bài.\n\n"
            "Em hãy viết câu lệnh vào khung bên trái rồi bấm **🚀 Nộp bài & Chấm điểm** nhé!"
        )

    # 2. Kiểm tra lỗi cú pháp bằng AST
    try:
        ast.parse(code_strip)
    except SyntaxError as e:
        err_line = e.lineno or 1
        lines = code_strip.splitlines()
        bad_line = lines[err_line - 1].strip() if err_line <= len(lines) else ""
        
        hint_text = "Cú pháp của câu lệnh chưa hợp lệ."
        if bad_line.startswith(("if ", "elif ", "else", "for ", "while ", "def ")) and not bad_line.endswith(":"):
            hint_text = f"Em đang thiếu **dấu hai chấm `:`** ở cuối câu lệnh `{bad_line}`."
        elif "expected an indented block" in str(e):
            hint_text = "Em quên chưa thụt đầu dòng (lùi vào 4 khoảng trắng) cho khối lệnh bên trong."
        elif "unmatched" in str(e).lower() or "was never closed" in str(e).lower():
            hint_text = "Em hãy kiểm tra lại các cặp ngoặc đơn `()` hoặc dấu nháy `''` đã đóng đủ chưa nhé."

        return (
            f"🔍 **Thầy/Cô phát hiện lỗi cú pháp tại Dòng {err_line}:**\n\n"
            f"- **Câu lệnh lỗi:** `{bad_line}`\n"
            f"- **Nguyên nhân & Cách sửa:** {hint_text}\n\n"
            "Em chỉnh lại đúng cú pháp rồi nộp lại bài nhé!"
        )

    # 3. Phân tích chi tiết lỗi theo kết quả Test Cases
    if "❌" in judge_details:
        diff_match = re.search(r"Đầu ra:\s*'([^']*)'\s*\|\s*Kỳ vọng:\s*'([^']*)'", judge_details)
        if diff_match:
            actual_str = diff_match.group(1)
            expected_str = diff_match.group(2)
            
            # Sai kiểu số thực / số nguyên
            if "." in actual_str and "." not in expected_str and actual_str.split(".")[0] == expected_str:
                return (
                    f"🔍 **Lưu ý kiểu dữ liệu xuất ra:**\n\n"
                    f"- Chương trình in ra số thực: `{actual_str}`\n"
                    f"- Nhưng đề bài yêu cầu số nguyên: `{expected_str}`\n\n"
                    "🛠️ **Cách sửa:** Em dùng hàm `int()` hoặc phép chia nguyên `//` để kết quả là số nguyên nhé!"
                )
            
            # Lỗi in nhiều dòng thay vì cùng 1 dòng
            if "\n" in actual_str and " " in expected_str:
                return (
                    "🔍 **Lưu ý cách hiển thị:**\n\n"
                    "- Đề bài yêu cầu in các số **trên cùng một dòng cách nhau khoảng trắng**.\n"
                    "- Chương trình của em đang ngắt xuống từng dòng riêng biệt.\n\n"
                    "🛠️ **Cách sửa:** Thêm tham số `end=' '` vào lệnh in: `print(giá_trị, end=' ')`."
                )

    # 4. Kiểm tra logic theo từng chủ đề
    if "hình thang" in full_info and "/" in code_strip:
        if "(a + b)" not in code_strip and "(a+b)" not in code_strip:
            return (
                "💡 **Lưu ý thứ tự phép toán:**\n\n"
                "Công thức diện tích hình thang là `(đáy lớn + đáy nhỏ) * chiều cao / 2`.\n"
                "Em cần đặt tổng 2 đáy trong ngoặc đơn `(a + b)` trước khi nhân chia, "
                "nếu không Python sẽ tính nhân chia trước cộng sau!"
            )

    if "nguyên tố" in full_info:
        return (
            "💡 **Hướng dẫn kiểm tra Số nguyên tố:**\n\n"
            "1. Số nguyên tố phải lớn hơn 1 và chỉ chia hết cho 1 và chính nó.\n"
            "2. Cho vòng lặp `for i in range(2, int(N**0.5) + 1):`.\n"
            "3. Nếu `N % i == 0` thì kết luận không phải số nguyên tố."
        )

    if "danh sách" in full_info or "mảng" in full_info:
        if "split" not in code_strip and "input" in code_strip:
            return (
                "💡 **Cách nhập dãy số thành danh sách (List):**\n\n"
                "Để nhận một dãy số cách nhau bởi khoảng trắng từ bàn phím, cú pháp chuẩn là:\n"
                "```python\n"
                "a = list(map(int, input().split()))\n"
                "```"
            )

    return (
        f"💡 **Thầy/Cô hướng dẫn em bài {title}:**\n\n"
        f"- **Yêu cầu:** {problem}\n"
        "- Em rà soát lại: biến khởi tạo, điều kiện lặp và câu lệnh in kết quả.\n"
        "- Sau khi chỉnh sửa, hãy bấm **🚀 Nộp bài & Chấm điểm** để kiểm tra lại nhé!"
    )

def get_gemini_socratic_response(user_prompt: str, context: dict) -> str:
    # -------------------------------------------------------------
    # 1. HỆ THỐNG KỶ LUẬT 3 LẦN (3-STRIKES LOCKOUT)
    # -------------------------------------------------------------
    if check_inappropriate_language(user_prompt):
        user = st.session_state.get("user", {})
        user_key = user.get("account_id") or user.get("email") or str(user.get("id", "guest"))

        strikes, is_locked = add_user_strike(user_key)

        if "user" in st.session_state and st.session_state.user:
            st.session_state.user["strikes"] = strikes
            if is_locked:
                st.session_state.user["is_locked"] = 1
                st.session_state.user["status"] = "Bị khóa do vi phạm kỷ luật"

        if is_locked or strikes >= 3:
            return (
                "🚫 **TÀI KHOẢN ĐÃ BỊ KHÓA TỰ ĐỘNG (VI PHẠM LẦN 3/3)!**\n\n"
                "Hệ thống EduCoder 10 ghi nhận em đã vi phạm chuẩn mực phát ngôn học đường 3 lần liên tiếp.\n\n"
                "- **Hình thức xử lý:** Toàn bộ quyền nộp bài và tương tác AI bị đình chỉ ngay lập tức.\n"
                "- **Yêu cầu:** Học sinh phải liên hệ trực tiếp Thầy/Cô bộ môn Tin học để giải trình."
            )
        elif strikes == 2:
            return (
                "🚨 **CẢNH BÁO NGUY CẤP (VI PHẠM LẦN 2/3)!**\n\n"
                "Hệ thống tiếp tục ghi nhận em sử dụng từ ngữ thô tục, thiếu chuẩn mực trong giờ học.\n\n"
                "- **Số lần vi phạm:** **2 / 3**\n"
                "- ⚠️ **LƯU Ý:** CHỈ CÒN DUY NHẤT 1 LẦN VI PHẠM NỮA, TÀI KHOẢN CỦA EM SẼ BỊ KHÓA VĨNH VIỄN!\n"
                "- Em hãy nghiêm túc tập trung vào bài làm và trao đổi lịch sự nhé!"
            )
        else:
            return (
                "⚠️ **CẢNH BÁO VI PHẠM KỶ LUẬT (LẦN 1/3)!**\n\n"
                "Hệ thống EduCoder 10 ghi nhận em vừa sử dụng từ ngữ thô tục, vi phạm quy chế học đường.\n\n"
                "- **Số lần vi phạm:** **1 / 3** (Điểm rèn luyện đã bị ghi nhận cảnh cáo).\n"
                "- **Quy chế:** Vi phạm đủ **3 lần**, hệ thống sẽ **TỰ ĐỘNG KHÓA TÀI KHOẢN**.\n\n"
                "Em hãy xóa bỏ các từ ngữ không phù hợp và hỏi về kiến thức bài học để Thầy/Cô hỗ trợ nhé!"
            )

    # -------------------------------------------------------------
    # 2. PHÂN TÍCH VÀ ĐƯA RA HƯỚNG DẪN CẶN KẼ
    # -------------------------------------------------------------
    student_code = context.get("student_code", "").strip()
    title = context.get("title", "")
    problem = context.get("problem", "")
    judge_details = context.get("judge_details", "")
    failed_line = context.get("failed_line", None)

    # Gọi Google Gemini nếu có cấu hình khóa API hợp lệ
    api_key = ""
    if hasattr(st, "secrets"):
        api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")

    if api_key and len(api_key.strip()) > 10 and not api_key.startswith("AQ.") and "AIzaSy..." not in api_key:
        try:
            genai.configure(api_key=api_key.strip())
            prompt_parts = [
                "Bạn là Trợ lý Sư phạm Tin học 10 chuyên nghiệp của EduCoder 10.",
                f"[BỐI CẢNH BÀI HỌC]: {title}",
                f"[ĐỀ BÀI]: {problem}",
                "[MÃ NGUỒN CỦA HỌC SINH]:",
                "```python",
                student_code,
                "```",
                f"[KẾT QUẢ TEST CASES]:\n{judge_details}",
                f"[DÒNG LỖI NGHI VẤN]: {failed_line}",
                f"[CÂU HỎI CỦA HỌC SINH]:\n\"{user_prompt}\"",
                "\nYÊU CẦU TRẢ LỜI:",
                "1. Xưng hô 'Thầy/Cô' và 'em'.",
                "2. Chỉ rõ chính xác dòng nào sai, sai vì sao (thiếu input, sai kiểu dữ liệu, sai công thức, thiếu dấu hai chấm).",
                "3. Hướng dẫn từng bước tư duy theo chuẩn SGK Tin học 10 mà không chép sẵn trọn vẹn lời giải."
            ]
            full_prompt = "\n".join(prompt_parts)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            res = model.generate_content(full_prompt)
            if res and res.text:
                return res.text
        except Exception:
            pass

    # Bộ phân tích sư phạm nội bộ (hoạt động tức thì 100% không lo mạng hay quota)
    return analyze_curriculum_exercise(student_code, title, problem, judge_details)