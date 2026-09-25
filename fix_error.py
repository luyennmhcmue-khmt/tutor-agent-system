import os
import ast

input_file = "extracted_sgk.py"
output_file = os.path.join("src", "sgk_data.py")

if not os.path.exists(input_file):
    exit()

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

cleaned_lines = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith("```"):
        continue
    if not stripped.startswith('"theory": """') and stripped not in ['"""', '""",']:
        line = line.replace('"""..."""', "'''...'''")
        line = line.replace('"""', "'''")
    
    cleaned_lines.append(line)

content = "".join(cleaned_lines).strip()

if "SGK_CURRICULUM = {" not in content:
    content = "SGK_CURRICULUM = {\n" + content

success = False
for patch in ["", "\n}\n", "\n    }\n}\n", '\n"""\n    }\n}\n']:
    trial = content + patch
    try:
        ast.parse(trial)
        content = trial
        success = True
        break
    except SyntaxError:
        continue

if not success:
    last_brace = content.rfind("}")
    if last_brace != -1:
        content = content[:last_brace + 1] + "\n"
        try:
            ast.parse(content)
            success = True
        except Exception as e:
            print(f"Lỗi: {e}")

os.makedirs("src", exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""DỮ LIỆU LÝ THUYẾT SGK TIN HỌC 10 KẾT NỐI TRI THỨC (GDPT 2018)"""\n\n')
    f.write(content.strip() + "\n")