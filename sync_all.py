import os
import re
import ast

if not os.path.exists("extracted_sgk.py"):
    exit()

with open("extracted_sgk.py", "r", encoding="utf-8") as f:
    raw_text = f.read()

clean_lines = [l for l in raw_text.splitlines() if not l.strip().startswith("```")]
cleaned = "\n".join(clean_lines)

cleaned = cleaned.replace('"""..."""', "'''...'''")
cleaned = cleaned.replace('"""', "'''", cleaned.count('"""') - (1 if cleaned.count('"""') % 2 != 0 else 0))

if "SGK_CURRICULUM = {" not in cleaned:
    match = re.search(r"SGK_CURRICULUM\s*=\s*\{", cleaned)
    if match:
        cleaned = cleaned[match.start():]
    else:
        cleaned = "SGK_CURRICULUM = {\n" + cleaned

if not cleaned.strip().endswith("}"):
    cleaned = cleaned.rstrip() + "\n}\n"

try:
    ast.parse(cleaned)
except Exception:
    for patch in ['\n"""\n    }\n}', '\n    }\n}', '\n}']:
        try:
            ast.parse(cleaned + patch)
            cleaned = cleaned + patch
            break
        except Exception:
            continue

os.makedirs("src", exist_ok=True)
sgk_data_path = os.path.join("src", "sgk_data.py")
with open(sgk_data_path, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""DỮ LIỆU LÝ THUYẾT CHUẨN SGK TIN HỌC 10 KẾT NỐI TRI THỨC (GDPT 2018)"""\n\n')
    f.write(cleaned.strip() + "\n")

scope = {}
try:
    exec(cleaned, scope)
    curriculum_dict = scope.get("SGK_CURRICULUM", {})
    print(f"🎉 ĐÃ XÁC NHẬN THÀNH CÔNG: {len(curriculum_dict)} bài học SGK chuẩn!")
    for code, data in list(curriculum_dict.items())[:4]:
        print(f"   ▶ [{code.upper()}] {data.get('name')}")
    print(f"   ... và {len(curriculum_dict) - 4} bài học tiếp theo.")
except Exception as e:
    print(f"⚠️ Cảnh báo nạp: {e}")

curriculum_file = os.path.join("src", "curriculum.py")
if os.path.exists(curriculum_file):
    with open(curriculum_file, "r", encoding="utf-8") as f:
        c_code = f.read()

    start_marker = "SGK_CURRICULUM = {"
    end_marker = "# 3. KHO 300 BÀI TẬP PYTHON"
    if end_marker not in c_code:
        end_marker = "def _build_curriculum_exercises():"

    if start_marker in c_code and end_marker in c_code:
        idx_start = c_code.find(start_marker)
        idx_end = c_code.find(end_marker)
        updated_curriculum = (
            c_code[:idx_start]
            + "from src.sgk_data import SGK_CURRICULUM\n\n# "
            + "-" * 73
            + "\n"
            + c_code[idx_end:]
        )
        with open(curriculum_file, "w", encoding="utf-8") as f:
            f.write(updated_curriculum)

if os.path.exists("app.py"):
    with open("app.py", "r", encoding="utf-8") as f:
        app_code = f.read()

    title_key = "CỐT LÕI KIẾN THỨC SGK TIN HỌC 10"
    if title_key in app_code:
        
        if "from src.sgk_data import SGK_CURRICULUM" not in app_code and "from src.curriculum import SGK_CURRICULUM" not in app_code:
            app_code = "from src.sgk_data import SGK_CURRICULUM\n" + app_code
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(app_code)