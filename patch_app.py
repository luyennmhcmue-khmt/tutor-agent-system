import os
import re

print("=" * 65)
print("🔍 ĐANG TÌM VÀ THAY THẾ ĐOẠN CODE CŨ TRONG DỰ ÁN...")
print("=" * 65)

target_files = ["app.py"] + [
    os.path.join("src", f) for f in os.listdir("src") if f.endswith(".py")
] if os.path.exists("src") else ["app.py"]

found = False

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Tìm file có chứa chuỗi sáo rỗng "in trần trụi" hoặc "ghi nhận câu hỏi"
    if "trần trụi" in content or "ghi nhận câu hỏi của em" in content:
        found = True
        print(f"🎯 ĐÃ PHÁT HIỆN ĐOẠN TEXT MẪU NẰM TRONG TỆP: '{file_path}'")
        
        # 1. Tìm hàm hoặc khối lệnh chứa đoạn gán phản hồi này
        lines = content.splitlines()
        start_line = 0
        end_line = 0
        for i, l in enumerate(lines):
            if "trần trụi" in l or "ghi nhận câu hỏi của em" in l:
                start_line = max(0, i - 8)
                end_line = min(len(lines), i + 8)
                break
        
        print("\n--- ĐOẠN MÃ CŨ ĐANG CHẠY: ---")
        for idx in range(start_line, end_line):
            print(f"{idx+1}: {lines[idx]}")
        print("-----------------------------\n")

if not found:
    print(" ")
    print(".")