# ==============================================================================
# LÝ THUYẾT & BÀI TẬP SGK TIN HỌC 10 - KẾT NỐI TRI THỨC VỚI CUỘC SỐNG
# ==============================================================================

SGK_CURRICULUM = {
    "c1": {
        "title": "Chương 1: Khái niệm cơ bản, Biến & Kiểu dữ liệu (Bài 16 - 18)",
        "name": "Chương 1: Khái niệm cơ bản, Biến & Kiểu dữ liệu (Bài 16 - 18)",
        "content": """
1. Kiểu dữ liệu cơ sở trong Python (Bài 16 - 18):
- int: Số nguyên (ví dụ: 15, -8).
- float: Số thực (ví dụ: 3.14, -0.5).
- str: Xâu ký tự, đặt trong nháy đơn hoặc nháy kép ('Tin 10', "Python").
- bool: Kiểu logic, chỉ nhận giá trị True hoặc False.

2. Biến và Lệnh gán (Bài 17):
- Cú pháp: <tên_biến> = <biểu_thức>. Tên biến không trùng từ khóa.
- Toán tử số học: +, -, *, / (chia thực), // (chia nguyên), % (chia dư), ** (lũy thừa).
- Toán tử logic: and, or, not.

3. Nhập/Xuất chuẩn (Bài 18):
- Hàm input() luôn trả về kiểu chuỗi (str). Bắt buộc ép kiểu: a = int(input()) hoặc x = float(input()).
- Hàm print(giá_trị_1, giá_trị_2, ...).
""",
        "theory": "Kiểu dữ liệu: int, float, str, bool. Nhập xuất: int(input()), print(). Toán tử: +, -, *, /, //, %, **."
    },
    "c2": {
        "title": "Chương 2: Cấu trúc rẽ nhánh if, if-else, if-elif-else (Bài 19)",
        "name": "Chương 2: Cấu trúc rẽ nhánh if, if-else, if-elif-else (Bài 19)",
        "content": """
1. Cấu trúc rẽ nhánh dạng thiếu:
if <điều_kiện>:
    <khối_lệnh>

2. Cấu trúc rẽ nhánh dạng đủ:
if <điều_kiện>:
    <khối_lệnh_1>
else:
    <khối_lệnh_2>

3. Cấu trúc rẽ nhánh nhiều nhánh (if-elif-else):
if <điều_kiện_1>:
    <khối_1>
elif <điều_kiện_2>:
    <khối_2>
else:
    <khối_cuối>

Lưu ý SGK: Cuối dòng if, elif, else bắt buộc có dấu hai chấm (:). Các câu lệnh trong cùng khối phải thụt lề 4 khoảng trắng.
""",
        "theory": "Cấu trúc rẽ nhánh: if, if-else, if-elif-else. Bắt buộc có dấu : ở cuối mệnh đề và thụt lề câu lệnh bên trong."
    },
    "c3": {
        "title": "Chương 3: Cấu trúc lặp for và while (Bài 20 - 21)",
        "name": "Chương 3: Cấu trúc lặp for và while (Bài 20 - 21)",
        "content": """
1. Vòng lặp for với số lần biết trước (Bài 20):
- Cú pháp: for <biến> in range(start, stop, step):
- range(n): chạy từ 0 đến n - 1.
- range(a, b): chạy từ a đến b - 1 (không chạm tới cận b).

2. Vòng lặp while với số lần chưa biết trước (Bài 21):
while <điều_kiện>:
    <khối_lệnh_lặp>

Lưu ý SGK: Cần có câu lệnh làm thay đổi giá trị điều kiện trong khối lặp để tránh lặp vô tận.
""",
        "theory": "Vòng lặp for: for i in range(a, b): chạy từ a đến b - 1. Vòng lặp while: while điều_kiện: lặp chừng nào điều kiện đúng."
    },
    "c4": {
        "title": "Chương 4: Kiểu dữ liệu Danh sách (List) (Bài 22 - 23)",
        "name": "Chương 4: Kiểu dữ liệu Danh sách (List) (Bài 22 - 23)",
        "content": """
1. Khởi tạo danh sách (Bài 22):
- Dãy phần tử đặt trong ngoặc vuông: A = [1, 3, 5, 'Tin 10'].
- Chỉ số đánh từ 0 đến len(A) - 1, hoặc chỉ số âm từ -1 (phần tử cuối).

2. Các thao tác cơ bản trên List (Bài 23):
- Thêm: A.append(x) (vào cuối), A.insert(vị_trí, x).
- Sửa: A[i] = giá_trị_mới.
- Xóa: del A[i], A.pop(i) hoặc A.remove(giá_trị).
- Hàm tiện ích: len(A), sum(A), min(A), max(A).
""",
        "theory": "Danh sách List: [1, 2, 3]. Các hàm cơ bản: append, insert, pop, remove, len, sum, min, max."
    },
    "c5": {
        "title": "Chương 5: Hàm và Chương trình con (Bài 26 - 28)",
        "name": "Chương 5: Hàm và Chương trình con (Bài 26 - 28)",
        "content": """
1. Định nghĩa và gọi hàm (Bài 26):
def tên_hàm(tham_số_1, tham_số_2):
    <khối_lệnh>
    return <kết_quả>

2. Phạm vi của biến (Bài 27 - 28):
- Biến cục bộ (Local): Khai báo bên trong hàm, chỉ có hiệu lực trong hàm đó.
- Biến toàn cục (Global): Khai báo bên ngoài hàm, truy xuất được từ mọi nơi. Muốn thay đổi biến toàn cục bên trong hàm phải dùng từ khóa global.
""",
        "theory": "Định nghĩa hàm: def tên_hàm(tham_số): ... return kết_quả. Biến cục bộ trong hàm, biến toàn cục ngoài hàm."
    },
    "c6": {
        "title": "Chương 6: Kiểm thử và Gỡ lỗi chương trình (Bài 29 - 30)",
        "name": "Chương 6: Kiểm thử và Gỡ lỗi chương trình (Bài 29 - 30)",
        "content": """
1. Phân loại lỗi chương trình (Bài 29):
- Lỗi cú pháp (Syntax Error): Quên dấu hai chấm (:), thiếu ngoặc, thụt lề sai (IndentationError).
- Lỗi ngoại lệ khi chạy (Runtime Error): Chia cho 0 (ZeroDivisionError), ép kiểu sai (ValueError), mảng vượt biên (IndexError).
- Lỗi ngữ nghĩa/logic (Semantic Error): Chương trình chạy không báo lỗi nhưng cho kết quả sai.

2. Kỹ thuật gỡ lỗi (Bài 30):
- Thiết kế Test Cases kiểm thử dữ liệu biên (0, số âm, mảng rỗng).
- Dùng lệnh print() trung gian theo dõi biến đổi giá trị của biến.
""",
        "theory": "Phân loại lỗi: SyntaxError, RuntimeError, SemanticError. Gỡ lỗi: Dùng Test Cases và lệnh print() trung gian."
    }
}

# ==============================================================================
# TẠO NGÂN HÀNG 300 BÀI TẬP (50 BÀI / CHƯƠNG)
# ==============================================================================
def build_300_exercises():
    ch_configs = [
        ("c1", "Khái niệm cơ bản & Kiểu dữ liệu", [
            "Tính giá trị biểu thức số học", "Quy đổi đơn vị đo độ dài và thời gian", "Tính chu vi diện tích hình chữ nhật",
            "Tách chữ số hàng đơn vị và hàng chục", "Ép kiểu nhập từ bàn phím", "Chia lấy dư tìm số dư phép chia",
            "Tính tiền điện năng tiêu thụ", "Nối ghép và xử lý chuỗi ký tự"
        ]),
        ("c2", "Cấu trúc rẽ nhánh if-else", [
            "Kiểm tra số chẵn hay số lẻ", "Tìm số lớn nhất trong ba số a, b, c", "Giải phương trình bậc nhất ax + b = 0",
            "Xếp loại học lực theo điểm", "Kiểm tra ba cạnh tam giác hợp lệ", "Tính cước taxi theo km",
            "Xác định năm nhuận", "Tính tiền lương tăng ca theo giờ"
        ]),
        ("c3", "Cấu trúc lặp for và while", [
            "In dãy số tự nhiên từ 1 đến n", "Tính tổng cấp số cộng S = 1 + ... + n", "Tính giai thừa n!",
            "Đếm số lượng ước số của n", "Kiểm tra số nguyên tố", "Tìm ước chung lớn nhất (UCLN)",
            "In bảng cửu chương của k", "Đảo ngược số nguyên dương bằng while"
        ]),
        ("c4", "Kiểu dữ liệu Danh sách (List)", [
            "Khởi tạo và xuất danh sách số nguyên", "Tìm phần tử lớn nhất trong List", "Tính tổng các phần tử dương",
            "Đếm phần tử chẵn trong List", "Chèn phần tử vào vị trí k", "Xóa các phần tử chẵn khỏi danh sách",
            "Tách danh sách chẵn lẻ", "Sắp xếp danh sách tăng dần"
        ]),
        ("c5", "Hàm và Chương trình con", [
            "Viết hàm tính lũy thừa a mũ n", "Hàm kiểm tra số chính phương", "Hàm tính diện tích tam giác Heron",
            "Hàm chuẩn hóa chuỗi họ tên", "Hàm tìm UCLN và BCNN", "Hàm đệ quy tính số Fibonacci",
            "Hàm đếm số từ trong câu", "Hàm lọc danh sách số nguyên tố"
        ]),
        ("c6", "Kiểm thử và Gỡ lỗi", [
            "Sửa lỗi SyntaxError quên dấu hai chấm", "Sửa lỗi IndentationError thụt lề sai", "Bắt ngoại lệ chia cho 0",
            "Xử lý lỗi ValueError khi nhập chuỗi", "Khắc phục lỗi IndexError mảng", "Gỡ lỗi lặp vô tận trong while",
            "Tạo bộ Test Cases kiểm thử tam giác", "Theo dõi biến bằng lệnh print trung gian"
        ])
    ]
    
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
    ex_dict = {}
    
    for ch_id, ch_title, topics in ch_configs:
        ex_dict[ch_id] = []
        for i in range(1, 51):
            topic = topics[(i - 1) % len(topics)]
            lvl = levels[(i - 1) % 4]
            code = f"{ch_id.upper()}_{i:02d}"
            ex_dict[ch_id].append({
                "id": code,
                "code": code,
                "title": f"Bài {i}: {topic}",
                "level": lvl,
                "problem": f"Viết chương trình Python giải quyết bài toán: {topic}. Dữ liệu nhập từ bàn phím chuẩn. Yêu cầu kiểm thử với các trường hợp dữ liệu hợp lệ.",
                "requirement": f"Viết chương trình Python giải quyết bài toán: {topic}. Dữ liệu nhập từ bàn phím chuẩn. Yêu cầu kiểm thử với các trường hợp dữ liệu hợp lệ.",
                "hint": f"Gợi ý sư phạm ({lvl}): Vận dụng kiến thức {ch_title}. Chú ý xác định rõ Input, xử lý biến và xuất Output đúng định dạng."
            })
    return ex_dict

CURRICULUM_EXERCISES = build_300_exercises()
# Tự động ánh xạ cả 2 tiền tố 'c' và 'ch' để tương thích 100% với app.py
for i in range(1, 7):
    c_k = f"c{i}"
    ch_k = f"ch{i}"
    if c_k in SGK_CURRICULUM:
        SGK_CURRICULUM[ch_k] = SGK_CURRICULUM[c_k]
    if c_k in CURRICULUM_EXERCISES:
        CURRICULUM_EXERCISES[ch_k] = CURRICULUM_EXERCISES[c_k]

# Đồng bộ dữ liệu dùng chung
SGK_THEORY = SGK_CURRICULUM
ALL_EXERCISES = CURRICULUM_EXERCISES