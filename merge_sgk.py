import re
import ast
try:
    with open("extracted_sgk.py", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    exit()

lines = [line for line in content.splitlines() if not line.strip().startswith("```")]
cleaned = "\n".join(lines)

cleaned = cleaned.replace('"""..."""', "'''...'''")
cleaned = cleaned.replace('"""', "'''", cleaned.count('"""') - (1 if cleaned.count('"""') % 2 != 0 else 0))

if not cleaned.strip().startswith("SGK_CURRICULUM = {"):
    match = re.search(r"SGK_CURRICULUM\s*=\s*\{", cleaned)
    if match:
        cleaned = cleaned[match.start():]
    else:
        cleaned = "SGK_CURRICULUM = {\n" + cleaned

if not cleaned.strip().endswith("}"):
    cleaned = cleaned.rstrip() + "\n}\n"

try:
    ast.parse(cleaned)
except Exception as err:
    if not cleaned.rstrip().endswith("}"):
        cleaned = cleaned.rstrip() + "\n    }\n}\n"

curriculum_path = "src/curriculum.py"
try:
    with open(curriculum_path, "r", encoding="utf-8") as f:
        curr_text = f.read()
except FileNotFoundError:
    exit()

start_marker = "SGK_CURRICULUM = {"
end_marker = "# 3. KHO 300 BÀI TẬP PYTHON"

if start_marker not in curr_text:
    exit()

if end_marker not in curr_text:
    end_marker = "def _build_curriculum_exercises():"

start_idx = curr_text.find(start_marker)
end_idx = curr_text.find(end_marker)

if end_idx == -1:
    exit()

prefix = curr_text[:start_idx]
suffix = curr_text[end_idx:]

new_curriculum_code = prefix + cleaned.strip() + "\n\n# " + "-" * 73 + "\n" + suffix

with open(curriculum_path, "w", encoding="utf-8") as f:
    f.write(new_curriculum_code)