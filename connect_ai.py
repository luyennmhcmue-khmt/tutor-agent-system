import re

print("=" * 65)
print("🚀 GIA SƯ ")
print("=" * 65)

with open("app.py", "r", encoding="utf-8") as f:
    app_text = f.read()

if "from src.strict_tutor import StrictSocraticMultiAgent" not in app_text:
    app_text = "from src.strict_tutor import StrictSocraticMultiAgent\n" + app_text

old_func_pattern = r"def get_step_by_step_scaffolding\([^\)]*\)[\s\S]*?(?=\ndef |\nclass |\n# ---|\nst\.|\Z)"

new_func_code = '''def get_step_by_step_scaffolding(exercise_info: dict, diag_tag: str = "", error_msg: str = "", student_code: str = "", student_question: str = "", chat_history: list = None) -> str:
    """Gia sư AI thực thụ: Đọc câu hỏi thực tế, phân tích code và chỉ lỗi bằng Gemini."""
    try:
        tutor = StrictSocraticMultiAgent()
        q = student_question.strip() if student_question else "Thầy/Cô hướng dẫn em cách làm bài này với ạ."
        if error_msg and not student_question:
            q = f"Bài của em gặp lỗi: {error_msg}. Thầy/Cô chỉ lỗi và hướng dẫn em cách sửa với ạ."
        
        res = tutor.generate_tutoring_turn(
            student_code=student_code,
            context_data=exercise_info,
            current_mastery=0.4,
            student_question=q,
            chat_history=chat_history or []
        )
        return res.get("tutor_response", "")
    except Exception as e:
        return f"Thầy/Cô ghi nhận câu hỏi. Em kiểm tra lại kết nối mạng nhé! (Lỗi: {e})"
'''

if "def get_step_by_step_scaffolding" in app_text:
    # Thay thế hàm cũ
    lines = app_text.splitlines()
    start_idx = None
    end_idx = None
    for idx, l in enumerate(lines):
        if l.startswith("def get_step_by_step_scaffolding"):
            start_idx = idx
            break
    
    if start_idx is not None:
        for idx in range(start_idx + 1, len(lines)):
            if (lines[idx].startswith("def ") or lines[idx].startswith("class ") or 
                (lines[idx] and not lines[idx].startswith(" ") and not lines[idx].startswith("\t") and not lines[idx].startswith("#"))):
                end_idx = idx
                break
        if end_idx is None:
            end_idx = len(lines)
            
        lines[start_idx:end_idx] = [new_func_code]
        app_text = "\n".join(lines)
        print("✅ Đã nâng cấp hàm get_step_by_step_scaffolding sang Gemini AI!")

mock_pattern = r'f[\"\']🤖\s*\*\*Trợ lý Socratic AI:\*\* Thầy/Cô đã ghi nhận câu hỏi[\s\S]*?Em cần thầy/cô kiểm tra giúp đoạn code cụ thể nào không\?[\"\']'

if re.search(r"Thầy/Cô đã ghi nhận câu hỏi của em", app_text):
    app_text = re.sub(
        r'f?"[^\n]*Thầy/Cô đã ghi nhận câu hỏi của em[^\n]*"',
        'ai_reply',
        app_text
    )
    print("✅ ")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_text)

print("\n HOÀN TẤT CẬP NHẬT!")