import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Sửa cảnh báo vàng: selected_exercise chưa khai báo
content = content.replace('"selected_exercise"', '"chosen_exercise"')
content = re.sub(
    r'current_ex\s*=\s*selected_exercise',
    'current_ex = locals().get("chosen_exercise", {})',
    content
)

# 2. Chuẩn hóa lại toàn bộ khối lọc bài tập từ filtered_exercises đến with col_detail:
pattern = r'[ \t]*filtered_exercises\s*=\s*\[[\s\S]*?with col_detail:'

replacement = '''        filtered_exercises = [
            ex for ex in REAL_EXERCISES
            if ex["chapter"] == selected_chapter and (selected_diff == "Tất cả" or ex.get("difficulty") == selected_diff)
        ]

        ex_options = [f"[{ex['id']}] {ex['title']}" for ex in filtered_exercises]
        if ex_options:
            selected_ex_str = st.selectbox("Chọn bài thực hành:", ex_options)
            selected_ex_id = selected_ex_str.split("]")[0].replace("[", "").strip()
            chosen_exercise = next((ex for ex in filtered_exercises if str(ex["id"]) == selected_ex_id), None)
        else:
            chosen_exercise = None

    with col_detail:'''

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content, count=1)
    print("✅ Đã chuẩn hóa thụt lề khối lọc bài tập!")
else:
    print("⚠️ Không khớp mẫu regex, vui lòng kiểm tra lại vị trí dòng.")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("🎉 XONG! Hãy kiểm tra lại tab Problems.")