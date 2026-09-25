import os
import glob
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    exit()

genai.configure(api_key=api_key)

pdf_files = glob.glob("data/*.pdf")
if not pdf_files:
    exit()

sgk_path = pdf_files[0]
for f in pdf_files:
    if "tin-hoc-10" in f.lower() or "sgk" in f.lower() or "kntt" in f.lower():
        sgk_path = f
        break

valid_models = []
try:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            valid_models.append(m.name)
except Exception as e:
    print(f"⚠️ Không thể liệt kê model qua API: {e}")

target_candidates = [
    "models/gemini-3.6-flash",
    "gemini-3.6-flash",
    "models/gemini-3.1-pro-preview",
    "models/gemini-2.0-flash"
]

chosen_model = None
for target in target_candidates:
    if target in valid_models or target.replace("models/", "") in [v.replace("models/", "") for v in valid_models]:
        chosen_model = target
        break

if not chosen_model and valid_models:
    chosen_model = valid_models[0]
elif not chosen_model:
    chosen_model = "gemini-3.6-flash"

uploaded_file = genai.upload_file(path=sgk_path)

while uploaded_file.state.name == "PROCESSING":
    time.sleep(2)
    uploaded_file = genai.get_file(uploaded_file.name)

prompt = """
Bạn là chuyên gia sư phạm Tin học. Hãy đọc toàn bộ cuốn Sách giáo khoa Tin học 10 (Bộ sách Kết nối tri thức với cuộc sống) trong file PDF vừa tải lên.

Nhiệm vụ:
Trích xuất tóm tắt lý thuyết của TẤT CẢ các bài học (từ Bài 1 đến Bài 32 theo đúng thứ tự Mục lục của sách).

YÊU CẦU ĐỊNH DẠNG:
Xuất ra đúng cú pháp từ điển Python có tên SGK_CURRICULUM:

SGK_CURRICULUM = {
    "b1": {
        "name": "Bài 1. Thông tin và xử lí thông tin",
        "chapter": "Chủ đề 1. Máy tính và xã hội tri thức",
        "theory": \"\"\"
### 1. ...
### 2. ...
### 3. ...
### 4. ...
\"\"\"
    },
    ...
}

QUY TẮC BẮT BUỘC:
1. Mỗi bài học đều PHẢI CÓ ĐỦ 4 MỤC (### 1., ### 2., ### 3., ### 4.), nội dung ngắn gọn, chuẩn xác theo SGK.
2. Tuyệt đối KHÔNG dùng 3 dấu nháy ngược (```) bên trong chuỗi theory; dùng thụt lề 4 dấu cách cho các dòng mã lệnh ví dụ.
3. Chỉ xuất nội dung mã nguồn Python bắt đầu từ SGK_CURRICULUM = { đến hết dấu }.
"""
model = genai.GenerativeModel(model_name=chosen_model)
response = model.generate_content([uploaded_file, prompt])

output_filename = "extracted_sgk.py"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(response.text)