import os
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

# Tự động nạp file .env ngay khi khởi động
load_dotenv()

from src.bkt_engine import DynamicKnowledgeTracing
from src.ast_engine import ASTAnalyzer

class StrictSocraticMultiAgent:
    """
    Tác tử Socratic AI - Người giáo viên Tin học 10 thực thụ:
    - Lắng nghe và phản hồi trực tiếp câu hỏi thực tế của học sinh.
    - Soi chiếu mã nguồn, chỉ rõ từng dòng lỗi (cú pháp, ép kiểu, logic).
    - Hướng dẫn thuật toán theo từng bài toán cụ thể bằng tư duy sư phạm gợi mở.
    - Tuyệt đối không viết hộ cả bài code giải sẵn (Zero-Code-Leak).
    """

    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
        self.api_key = key.strip() if key else ""

        self.bkt = DynamicKnowledgeTracing()
        self.ast_analyzer = ASTAnalyzer()

        # Danh sách mô hình theo chuẩn mới nhất của Google
        self.primary_model = "gemini-3.6-flash"
        self.fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def generate_tutoring_turn(
        self,
        student_code: str = "",
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Tiếp nhận linh hoạt mọi kiểu gọi từ app.py."""
        context_data = {}
        current_mastery = 0.5
        student_question = ""
        chat_history = []

        # 1. Bóc tách an toàn các đối số truyền theo vị trí
        if len(args) >= 1:
            if isinstance(args[0], dict):
                context_data = args[0]
            elif isinstance(args[0], (int, float)):
                current_mastery = float(args[0])
            elif isinstance(args[0], str):
                student_question = args[0]

        if len(args) >= 2:
            if isinstance(args[1], (int, float)):
                try:
                    current_mastery = float(args[1])
                except Exception:
                    pass
            elif isinstance(args[1], str):
                student_question = args[1]
            elif isinstance(args[1], dict):
                context_data = args[1]

        if len(args) >= 3:
            if isinstance(args[2], str):
                student_question = args[2]
            elif isinstance(args[2], (int, float)):
                try:
                    current_mastery = float(args[2])
                except Exception:
                    pass

        # 2. Ghi đè nếu truyền qua tham số từ khóa kwargs
        if "context_data" in kwargs and kwargs["context_data"]:
            if isinstance(kwargs["context_data"], dict):
                context_data.update(kwargs["context_data"])
        if "exercise_info" in kwargs and kwargs["exercise_info"]:
            if isinstance(kwargs["exercise_info"], dict):
                context_data.update(kwargs["exercise_info"])
        if "current_mastery" in kwargs and kwargs["current_mastery"] is not None:
            try:
                current_mastery = float(kwargs["current_mastery"])
            except Exception:
                current_mastery = 0.5
        if "student_question" in kwargs and kwargs["student_question"]:
            student_question = str(kwargs["student_question"])
        if "chat_history" in kwargs and kwargs["chat_history"]:
            chat_history = kwargs["chat_history"]

        # 3. Phân tích cú pháp tĩnh AST từ mã nguồn học sinh
        ast_result = self.ast_analyzer.analyze(student_code)
        syntax_valid = ast_result.get("syntax_valid", True)
        detected_patterns = ast_result.get("detected_patterns", [])

        # 4. Xác định cấp độ giàn giáo từ BKT
        scaffold_level = self.bkt.determine_scaffolding_level(
            mastery_score=current_mastery,
            syntax_valid=syntax_valid
        )

        # 5. Trích xuất thông tin bài tập hiện tại
        ex_title = context_data.get("title") or context_data.get("name") or "Bài tập lập trình Python"
        ex_desc = context_data.get("description") or context_data.get("problem_statement") or "Chưa có mô tả chi tiết"
        ex_concept = context_data.get("concept") or context_data.get("topic") or "Kiến thức trọng tâm"

        # 6. Biên tập lịch sử hội thoại gần nhất
        formatted_history = ""
        if chat_history and isinstance(chat_history, list):
            recent = chat_history[-6:]
            for turn in recent:
                if isinstance(turn, dict):
                    role = "Học sinh" if turn.get("role") == "user" else "Thầy/Cô"
                    formatted_history += f"{role}: {turn.get('content')}\n"

        # 7. Chuẩn bị chẩn đoán cú pháp kỹ thuật
        if not syntax_valid:
            ast_diagnostic = (
                f"LỖI CÚ PHÁP PHÁT HIỆN TẠI DÒNG {ast_result.get('error_line')}, CỘT {ast_result.get('error_col')}:\n"
                f"- Chi tiết lỗi: {ast_result.get('error_msg')}\n"
                f"- Dòng code bị lỗi: {ast_result.get('error_text', '')}"
            )
        else:
            ast_diagnostic = "Cú pháp hợp lệ (Không có lỗi biên dịch SyntaxError)."
            notes = []
            if "missing_input_type_cast" in detected_patterns:
                notes.append("Dùng input() nhưng chưa ép kiểu int() hoặc float() để tính toán/chạy vòng lặp.")
            if "potential_infinite_loop" in detected_patterns:
                notes.append("Vòng lặp while True không có lệnh break hoặc điều kiện thoát.")
            if "string_mutation_attempt" in detected_patterns:
                notes.append("Cố gán lại ký tự của xâu s[i] = ... (Xâu trong Python là bất biến).")
            if notes:
                ast_diagnostic += "\nLưu ý phân tích: " + "; ".join(notes)

        clean_code = student_code.strip() if student_code and student_code.strip() else "# (Học sinh chưa nhập dòng mã nào)"

        # 8. Hướng dẫn sư phạm (System Instruction)
        system_instruction = f"""
Bạn là Giáo viên Gia sư Tin học 10 chuyên nghiệp theo chương trình GDPT 2018 (SGK Kết nối tri thức).
Xưng hô: Luôn xưng "Thầy/Cô" và gọi "Em". Giọng điệu điềm đạm, ân cần, tôn trọng học sinh.

THÔNG TIN BÀI TẬP HIỆN TẠI:
- Tên bài: {ex_title}
- Đề bài: {ex_desc}
- Chủ đề: {ex_concept}
- Năng lực học sinh: Mức {int(current_mastery * 100)}% (Giàn giáo cấp {scaffold_level}/3)

NGUYÊN TẮC SƯ PHẠM BẮT BUỘC:
1. TRẢ LỜI ĐÚNG TRỌNG TÂM CÂU HỎI THỰC TẾ:
   - Tuyệt đối không dùng các câu khẩu hiệu rập khuôn sáo rỗng.
   - Trả lời thẳng vào nội dung học sinh hỏi và bám sát bài toán "{ex_title}".

2. XỬ LÝ THEO TÌNH HUỐNG:
   - Học sinh chưa biết làm / hỏi cách làm:
     + Giải thích tư duy bài toán bằng hình tượng thực tế.
     + Chia nhỏ thành 3 bước: Bước 1 (Nhập dữ liệu), Bước 2 (Xử lý thuật toán), Bước 3 (In kết quả).
     + Hướng dẫn học sinh viết câu lệnh cho Bước 1 trước.
   - Code bị sai cú pháp hoặc logic:
     + Dựa vào chẩn đoán AST, chỉ rõ dòng bị sai và giải thích nguyên nhân.
     + Hướng dẫn cách sửa tư duy logic mà không chép code sửa sẵn.
   - Học sinh hỏi về câu lệnh cụ thể:
     + Giải thích bản chất từng thành phần trong câu lệnh đó.

3. NGUYÊN TẮC ZERO-CODE-LEAK:
   - Tuyệt đối không viết trọn vẹn cả bài code hoàn chỉnh cho học sinh chép.
   - Chỉ minh họa cú pháp tổng quát (ví dụ: for item in danh_sach:).
   - Luôn kết thúc bằng một câu hỏi gợi mở để học sinh tự tay viết mã vào khung soạn thảo.
"""

        # 9. Soạn câu hỏi của người dùng gửi tới AI
        user_prompt = f"""
[LỊCH SỬ TRAO ĐỔI]
{formatted_history if formatted_history else '(Chưa có trao đổi trước đó)'}

[MÃ NGUỒN HIỆN TẠI CỦA HỌC SINH]
=== BẮT ĐẦU MÃ NGUỒN ===
{clean_code}
=== KẾT THÚC MÃ NGUỒN ===

[KẾT QUẢ PHÂN TÍCH KỸ THUẬT AST]
{ast_diagnostic}

[CÂU HỎI CỦA HỌC SINH]
"{student_question if student_question.strip() else 'Thầy/Cô hướng dẫn em cách làm bài này với ạ.'}"

Hãy đóng vai người giáo viên thực thụ, đọc kỹ câu hỏi và bài làm để hướng dẫn học sinh một cách chân thực, đúng trọng tâm:
"""

        # 10. Thực thi gọi mô hình Gemini
        raw_response = self._call_gemini_api(system_instruction, user_prompt)
        safe_response = self._guardrail_verification(raw_response)

        return {
            "tutor_response": safe_response,
            "scaffold_level": scaffold_level,
            "ast_valid": syntax_valid,
            "ast_summary": ast_result.get("summary")
        }

    def _call_gemini_api(self, system_instruction: str, prompt: str) -> str:
        """Thực hiện gọi API với cơ chế dự phòng nhiều tầng model."""
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")

        if not self.api_key:
            return (
                "⚠️ **Thông báo:** Chưa tìm thấy `GEMINI_API_KEY` trong tệp `.env`. "
                "Em hãy kiểm tra lại cấu hình khóa API để kích hoạt Thầy/Cô AI nhé!"
            )

        if not self.client:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                pass

        # 1. Ưu tiên SDK mới
        models_to_try = [self.primary_model] + self.fallback_models
        if self.client:
            for model_name in models_to_try:
                try:
                    resp = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config={
                            "system_instruction": system_instruction,
                            "temperature": 0.25
                        }
                    )
                    if resp and resp.text and resp.text.strip():
                        return resp.text.strip()
                except Exception:
                    continue

        # 2. Dự phòng SDK cũ nếu SDK mới chưa nạp
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.api_key)
            for m in ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    legacy_model = legacy_genai.GenerativeModel(
                        model_name=m,
                        system_instruction=system_instruction
                    )
                    r = legacy_model.generate_content(prompt)
                    if r and r.text and r.text.strip():
                        return r.text.strip()
                except Exception:
                    continue
        except Exception as e:
            return f"⚠️ **Lỗi kết nối AI:** {str(e)}. Em hãy kiểm tra kết nối mạng nhé!"

        return "Thầy/Cô đã nắm được câu hỏi của em. Em hãy kiểm tra lại mạng và bấm hỏi lại để thầy/cô hướng dẫn chi tiết nhé!"

    def _guardrail_verification(self, text: str) -> str:
        """Ngăn chặn AI giải hộ toàn bộ bài tập."""
        if not text:
            return text

        code_blocks = re.findall(r"```(?:python)?\s*([\s\S]*?)```", text)
        for block in code_blocks:
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            has_io = any("input" in l for l in lines) and any("print" in l for l in lines)
            if len(lines) >= 4 or (has_io and len(lines) >= 3):
                replacement = (
                    "\n> *(Thầy/Cô sẽ không viết sẵn cả bài giải hoàn chỉnh cho em, "
                    "vì tự tay tư duy và gõ lệnh mới giúp em tiến bộ thực sự!)*\n\n"
                    "👉 **Gợi ý bước tiếp theo:** Em hãy đọc hướng dẫn ở trên, viết câu lệnh vào khung code rồi bấm 'Kiểm tra' để thầy/cô xem cùng em nhé!"
                )
                return re.sub(r"```(?:python)?\s*[\s\S]*?```", replacement, text)

        return text