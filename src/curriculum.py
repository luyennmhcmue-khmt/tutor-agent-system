"""
src/curriculum.py - Dữ liệu cốt lõi chương trình Tin học 10 (GDPT 2018)
Bao gồm:
1. CHAPTER_NAMES: Tên chi tiết 5 chương học
2. SGK_CURRICULUM: Cốt lõi lý thuyết Bài 16 - Bài 30 chuẩn sư phạm
3. CURRICULUM_EXERCISES: Đầy đủ 300 bài tập thực hành phân cấp độ (kèm testcases)
"""

import json

# ------------------------------------------------------------------------------
# 1. TÊN CHI TIẾT 5 CHƯƠNG HỌC (GDPT 2018)
# ------------------------------------------------------------------------------
CHAPTER_NAMES = {
    "c1": "Chương 1: Làm quen với Python & Các lệnh vào ra cơ bản (Bài 16 - 18)",
    "c2": "Chương 2: Cấu trúc rẽ nhánh if - else (Bài 19)",
    "c3": "Chương 3: Cấu trúc lặp for và while (Bài 20 - 21)",
    "c4": "Chương 4: Kiểu dữ liệu danh sách List (Bài 22 - 23)",
    "c5": "Chương 5: Xâu ký tự & Hàm trong Python (Bài 24 - 30)"
}

# ------------------------------------------------------------------------------
# 2. CỐT LÕI KIẾN THỨC SGK TIN HỌC 10 (BÀI 16 - 30)
# ------------------------------------------------------------------------------
SGK_CURRICULUM = {
    "b16": {
        "name": "Bài 16: Ngôn ngữ lập trình bậc cao và Python",
        "content": """### 1. Đặc điểm ngôn ngữ lập trình bậc cao
- Ngôn ngữ bậc cao có cú pháp gần gũi với ngôn ngữ tự nhiên (tiếng Anh), độc lập với thiết bị phần cứng.
- Python là ngôn ngữ lập trình bậc cao, mã nguồn mở, đa nền tảng và có cú pháp rõ ràng, dễ tiếp cận.

### 2. Hai chế độ làm việc trong Python
- **Chế độ tương tác (Shell):** Gõ từng dòng lệnh tại dấu nhắc `>>>` và nhận kết quả tức thì.
- **Chế độ soạn thảo (Script):** Viết tập hợp câu lệnh trong tệp `.py` và thực thi toàn bộ chương trình.

### 3. Lệnh xuất dữ liệu đầu tiên
    print("Xin chào Python!")

*Lưu ý: Python phân biệt chữ hoa và chữ thường (`print` khác `Print`).*"""
    },
    "b17": {
        "name": "Bài 17: Biến và lệnh gán",
        "content": """### 1. Quy tắc đặt tên biến trong Python
- Tên biến chỉ chứa chữ cái, chữ số và dấu gạch dưới `_`.
- Ký tự đầu tiên bắt buộc phải là chữ cái hoặc dấu gạch dưới, không được bắt đầu bằng chữ số.
- Tên biến không được trùng với từ khóa mặc định (`if`, `else`, `for`, `def`, `while`...).

### 2. Các kiểu dữ liệu cơ sở & Phép toán
- `int`: Số nguyên | `float`: Số thực | `str`: Xâu ký tự | `bool`: Đúng/Sai (`True`/`False`).
- Phép toán số học: `+`, `-`, `*`, `/` (chia thực), `//` (chia nguyên), `%` (chia dư), `**` (lũy thừa)."""
    },
    "b18": {
        "name": "Bài 18: Các lệnh vào ra đơn giản",
        "content": """### 1. Lệnh nhập dữ liệu từ bàn phím
- Cú pháp: `biến = input()`
- **Quy tắc bất biến:** Giá trị trả về từ lệnh `input()` luôn luôn là kiểu chuỗi (`str`).

### 2. Ép kiểu bắt buộc khi tính toán số học
- Số nguyên: `a = int(input())`
- Số thực: `x = float(input())`

### 3. Lệnh xuất dữ liệu
- Cú pháp chuẩn: `print(giá_trị_1, giá_trị_2, sep=' ', end='\\n')`"""
    },
    "b19": {
        "name": "Bài 19: Câu lệnh rẽ nhánh if",
        "content": """### 1. Cấu trúc rẽ nhánh dạng thiếu và đủ
    # Dạng thiếu
    if <điều_kiện>:
        <khối_lệnh>

    # Dạng đủ
    if <điều_kiện>:
        <khối_lệnh_1>
    else:
        <khối_lệnh_2>

### 2. Quy tắc cú pháp bắt buộc
- Cuối dòng `if`, `elif`, `else` bắt buộc phải có dấu hai chấm `:`.
- Khối lệnh bên trong phải thụt lề đồng nhất 4 khoảng trắng."""
    },
    "b20": {
        "name": "Bài 20: Câu lệnh lặp for",
        "content": """### 1. Vòng lặp với số lần biết trước
    for <biến_chạy> in range(start, stop, step):
        <khối_lệnh_lặp>

### 2. Ý nghĩa hàm range()
- `range(n)`: Chạy từ `0` đến `n - 1` (tổng cộng `n` lần).
- `range(a, b)`: Chạy từ `a` đến `b - 1` (không chạm tới `b`).
- `range(a, b, step)`: Chạy từ `a` đến trước `b` với bước nhảy `step`."""
    },
    "b21": {
        "name": "Bài 21: Câu lệnh lặp while",
        "content": """### 1. Vòng lặp với số lần chưa biết trước
    while <điều_kiện>:
        <khối_lệnh_lặp>

### 2. Kiểm soát vòng lặp vô hạn (TLE)
- Trong thân vòng lặp `while`, bắt buộc phải có lệnh cập nhật biến điều kiện để biểu thức chuyển sang `False` khi thỏa mãn điều kiện dừng."""
    },
    "b22": {
        "name": "Bài 22: Kiểu dữ liệu danh sách (List)",
        "content": """### 1. Khái niệm và khởi tạo
- Danh sách là tập hợp các phần tử có thứ tự, đặt trong cặp ngoặc `[]`. Ví dụ: `a = [10, 20, 30]`.

### 2. Chỉ số (Index) trong Python
- Chỉ số dương: Từ `0` đến `len(a) - 1`.
- Chỉ số âm: `-1` là phần tử cuối cùng của danh sách."""
    },
    "b23": {
        "name": "Bài 23: Một số lệnh làm việc với dữ liệu danh sách",
        "content": """### 1. Các phương thức danh sách thông dụng
- `a.append(x)`: Thêm `x` vào cuối danh sách.
- `a.insert(i, x)`: Chèn `x` vào vị trí `i`.
- `a.remove(x)`: Xóa phần tử đầu tiên có giá trị `x`.
- `del a[i]` hoặc `a.pop(i)`: Xóa phần tử theo vị trí chỉ số.

### 2. Các hàm thống kê có sẵn
- `len(a)`: Độ dài danh sách.
- `sum(a)`: Tổng các phần tử số.
- `min(a)`, `max(a)`: Giá trị nhỏ nhất, lớn nhất."""
    },
    "b24": {
        "name": "Bài 24: Xâu kí tự (String)",
        "content": """### 1. Khái niệm xâu kí tự
- Xâu là dãy kí tự đặt trong cặp ngoặc nháy đơn `''` hoặc nháy kép `""`.
- Xâu trong Python là đối tượng **bất biến (immutable)**.

### 2. Phép toán và cắt lát (Slicing)
- Ghép xâu: `s1 + s2` | Lặp xâu: `s * 3`
- Cắt lát xâu: `s[start:stop:step]` (Ví dụ đảo ngược: `s[::-1]`)."""
    },
    "b25": {
        "name": "Bài 25: Một số lệnh làm việc với xâu kí tự",
        "content": """### 1. Các phương thức xử lý xâu phổ biến
- `s.split()`: Tách xâu thành danh sách từ theo dấu cách.
- `' '.join(list_tu)`: Nối danh sách các từ thành xâu.
- `s.lower()`, `s.upper()`: Chuyển đổi chữ thường, chữ hoa.
- `s.find(sub)`: Tìm vị trí xuất hiện đầu tiên của chuỗi con `sub`."""
    },
    "b26": {
        "name": "Bài 26: Hàm trong Python",
        "content": """### 1. Định nghĩa và gọi hàm
    def ten_ham(tham_so):
        # Khối lệnh xử lý
        return gia_tri

### 2. Lệnh return
- Trả về kết quả cho nơi gọi và lập tức kết thúc hàm. Nếu không có `return`, hàm trả về `None`."""
    },
    "b27": {
        "name": "Bài 27: Tham số của hàm",
        "content": """### 1. Tham số hình thức và thực sự
- **Tham số hình thức:** Biến khai báo trong định nghĩa hàm.
- **Tham số thực sự:** Giá trị cụ thể truyền vào hàm khi gọi thực thi.

### 2. Tham số mặc định
    def chao(ten, loi_chao="Xin chào"):
        print(loi_chao, ten)"""
    },
    "b28": {
        "name": "Bài 28: Phạm vi của biến",
        "content": """### 1. Biến cục bộ (Local)
- Khai báo bên trong hàm, chỉ có hiệu lực và sử dụng được bên trong thân hàm đó.

### 2. Biến toàn cục (Global)
- Khai báo ngoài các hàm. Sử dụng từ khóa `global <tên_biến>` khi cần sửa đổi giá trị biến toàn cục từ trong thân hàm."""
    },
    "b29": {
        "name": "Bài 29: Nhận biết lỗi chương trình",
        "content": """### 1. Ba nhóm lỗi thường gặp
- **SyntaxError (Lỗi cú pháp):** Vi phạm quy tắc viết code (thiếu `:`, thiếu ngoặc).
- **RuntimeError (Lỗi khi chạy):** Lỗi chia cho 0 (`ZeroDivisionError`), ép kiểu sai (`ValueError`).
- **SemanticError (Lỗi ngữ nghĩa/logic):** Chương trình chạy bình thường nhưng kết quả sai yêu cầu."""
    },
    "b30": {
        "name": "Bài 30: Kiểm thử và gỡ lỗi chương trình",
        "content": """### 1. Kiểm thử chương trình (Testing)
- Thiết kế các bộ kiểm thử (Test Cases) bao gồm: Dữ liệu thông thường, Dữ liệu biên (biên 0, số âm, danh sách rỗng).

### 2. Kỹ thuật gỡ lỗi (Debugging)
- Chèn lệnh `print()` trung gian để theo dõi sự biến đổi giá trị của các biến trong từng bước thực thi."""
    }
}

# ------------------------------------------------------------------------------
# 3. KHO 300 BÀI TẬP PYTHON (GDPT 2018) - 5 CHƯƠNG x 60 BÀI / CHƯƠNG = 300 BÀI
# ------------------------------------------------------------------------------
def _build_curriculum_exercises():
    exercises = {f"c{i}": [] for i in range(1, 6)}
    levels = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]

    bank = {
        "c1": {
            "Nhận biết": [
                ("In dòng chữ xin chào ra màn hình", "Dùng print('Xin chào')", "1\n1", "Xin chào"),
                ("Tính tổng hai số nguyên a và b", "Dùng int(input()) và phép toán +", "3\n5", "8"),
                ("Tính hiệu của hai số nguyên a và b", "Dùng phép toán trừ -", "10\n4", "6"),
                ("Tính tích của hai số nguyên a và b", "Dùng phép toán nhân *", "6\n7", "42"),
                ("Tính bình phương của một số nguyên N", "Dùng N ** 2", "5", "25"),
                ("Tính lập phương của một số nguyên N", "Dùng N ** 3", "3", "27"),
                ("Tính chu vi hình vuông cạnh a", "Chu vi = a * 4", "4", "16"),
                ("Tính diện tích hình vuông cạnh a", "Diện tích = a * a", "5", "25"),
                ("Tìm số liền sau của số nguyên N", "In ra N + 1", "9", "10"),
                ("Tìm số liền trước của số nguyên N", "In ra N - 1", "9", "8"),
                ("Đổi số giờ sang số phút", "Số phút = số giờ * 60", "2", "120"),
                ("Đổi số ngày sang số giờ", "Số giờ = số ngày * 24", "3", "72"),
                ("Tính gấp ba lần một số nguyên N", "In ra N * 3", "7", "21"),
                ("Lấy phần nguyên phép chia a cho b", "Dùng toán tử chia nguyên //", "17\n5", "3"),
                ("Lấy phần dư phép chia a cho b", "Dùng toán tử chia dư %", "17\n5", "2")
            ],
            "Thông hiểu": [
                ("Tính chu vi và diện tích hình chữ nhật", "Chu vi = (a+b)*2, DT = a*b", "4\n5", "18\n20"),
                ("Tính thương phép chia thực hai số", "Dùng toán tử chia /", "7\n2", "3.5"),
                ("Tính trung bình cộng 2 số nguyên", "Tổng chia cho 2", "4\n6", "5.0"),
                ("Chia đều kẹo và tìm số kẹo còn dư", "Dùng // và %", "14\n4", "3\n2"),
                ("Đổi phút sang định dạng giờ và phút", "Dùng // 60 và % 60", "125", "2 gio 5 phut"),
                ("Tính tiền mua vở theo số lượng và đơn giá", "Thành tiền = số lượng * đơn giá", "10\n5000", "50000"),
                ("Tính tiền thừa trả khách khi mua hàng", "Tiền thừa = Tiền khách đưa - Trị giá đơn", "100000\n75000", "25000"),
                ("Tính diện tích tam giác biết đáy và chiều cao", "DT = (đáy * cao) / 2", "6\n4", "12.0"),
                ("Tính chu vi hình tròn bán kính R", "Chu vi = 2 * 3.14 * R", "5", "31.4"),
                ("Tính diện tích hình tròn bán kính R", "DT = 3.14 * R * R", "10", "314.0"),
                ("Tính vận tốc trung bình qua quãng đường và thời gian", "Vận tốc = S / t", "100\n2", "50.0"),
                ("Tính tổng chữ số của số nguyên có hai chữ số", "Hàng chục n // 10, đơn vị n % 10", "47", "11"),
                ("Đổi độ C sang độ F", "F = C * 1.8 + 32", "0", "32.0"),
                ("Tính chu vi hình thang", "Tổng 4 cạnh", "3\n5\n2\n2", "12"),
                ("Tính diện tích hình thang", "DT = (đáy lớn + đáy nhỏ) * cao / 2", "4\n6\n3", "15.0")
            ],
            "Vận dụng": [
                ("Đổi giây sang định dạng giờ, phút, giây", "Dùng // 3600, // 60 và %", "3665", "1 gio 1 phut 5 giay"),
                ("Tính tiền gửi tiết kiệm lãi đơn sau N tháng", "Lãi = Gốc * Lãi suất * N", "1000000\n0.05\n12", "600000.0"),
                ("Tính tổng 3 chữ số của số nguyên N", "Dùng // 100, // 10 % 10 và % 10", "123", "6"),
                ("Đảo ngược số nguyên có 2 chữ số", "In hàng đơn vị trước hàng chục", "37", "73"),
                ("Tính độ dài cạnh huyền theo định lý Pythagoras", "c = (a**2 + b**2)**0.5", "3\n4", "5.0"),
                ("Tính tiền điện theo đơn giá cố định", "Nhập số kWh cũ và mới, nhân đơn giá", "120\n150\n2000", "60000"),
                ("Tính tiền nước sinh hoạt gia đình", "Nhân khối lượng tiêu thụ với đơn giá", "15\n12000", "180000"),
                ("Tính chỉ số khối cơ thể BMI", "BMI = cân nặng / (chiều cao ** 2)", "50\n1.6", "19.53"),
                ("Tính quãng đường rơi tự do s = 0.5*g*t^2", "Với g = 9.8", "2", "19.6"),
                ("Tính năng lượng tiêu hao theo công suất và thời gian", "A = P * t", "1000\n3", "3000"),
                ("Tính tổng các số tự nhiên từ 1 đến N bằng công thức", "S = N * (N + 1) // 2", "10", "55"),
                ("Tính giá trị đa thức bậc hai ax^2 + bx + c", "Thay x vào đa thức", "1\n2\n1\n3", "16"),
                ("Bài toán chia tổ phân đều học sinh", "Tìm số học sinh mỗi tổ và dư", "43\n4", "10\n3"),
                ("Tính diện tích tam giác theo công thức Heron", "p = (a+b+c)/2; S = sqrt(p(p-a)(p-b)(p-c))", "3\n4\n5", "6.0"),
                ("Tính khoảng cách Euclidean giữa hai điểm 1D", "Khoảng cách = abs(x2 - x1)", "10\n4", "6")
            ],
            "Vận dụng cao": [
                ("Tính số lượng tờ tiền tối thiểu đổi mệnh giá", "Tham lam từ mệnh giá lớn đến bé", "128", "1 to 100k, 1 to 20k, 1 to 5k, 3 to 1k"),
                ("Tính số chuyến xe buýt tối thiểu để chở N người", "Dùng phép chia trần (N + C - 1) // C", "45\n10", "5"),
                ("Tính số gạch vuông cần mua để lát kín nền", "Lấy trần diện tích chia gạch", "20\n30\n5", "24"),
                ("Tính tổng các chữ số của số có 4 chữ số", "Tách từng hàng nghìn, trăm, chục, đơn vị", "2026", "10"),
                ("Xác định thời gian đồng hồ sau K phút", "Cộng phút và lấy modulo 24 giờ", "8\n30\n45", "9:15"),
                ("Tính góc tạo bởi kim giờ và kim phút", "Góc = abs(30*h - 5.5*m)", "3\n0", "90.0"),
                ("Tính lượng sơn phủ bề mặt hình lập phương", "6 * a * a nhân hệ số", "3\n0.2", "10.8"),
                ("Tính tọa độ trung điểm của đoạn thẳng 2D", "x = (x1+x2)/2, y = (y1+y2)/2", "0\n0\n4\n6", "2.0 3.0"),
                ("Tính khoảng cách giữa 2 điểm trong mặt phẳng 2D", "Dùng căn tổng bình phương hiệu", "0\n0\n3\n4", "5.0"),
                ("Xác định số can nước 5L cần để đong đầy thùng L lít", "Phép chia làm tròn lên", "18", "4"),
                ("Tính tổng chuỗi cấp số nhân đơn giản", "a * (r**n - 1) // (r - 1)", "2\n2\n3", "14"),
                ("Tìm số dư của lũy thừa chia cho 10", "Dùng toán tử % 10", "7\n3", "3"),
                ("Tính diện tích phần tô đậm giữa hình vuông và hình tròn nội tiếp", "a*a - 3.14*(a/2)**2", "4", "3.44"),
                ("Đổi tiền xu tối ưu 3 mệnh giá", "Quy đổi theo thứ tự 10, 5, 1", "27", "2 to 10, 1 to 5, 2 to 1"),
                ("Tính ngày trong tuần sau N ngày", "(hôm_nay + N) % 7", "2\n10", "5")
            ]
        },
        "c2": {
            "Nhận biết": [
                ("Kiểm tra số nguyên N là chẵn hay lẻ", "Dùng if N % 2 == 0", "4", "CHAN"),
                ("Tìm số lớn nhất trong hai số nguyên a và b", "Dùng if a > b", "7\n3", "7"),
                ("Tìm số nhỏ nhất trong hai số nguyên a và b", "Dùng if a < b", "7\n3", "3"),
                ("Kiểm tra số nguyên N là âm hay dương", "Dùng if N > 0", "5", "DUONG"),
                ("Kiểm tra số nguyên N có bằng 0 hay không", "Dùng if N == 0", "0", "BANG 0"),
                ("Kiểm tra N có chia hết cho 5 không", "Dùng if N % 5 == 0", "25", "CHIA HET"),
                ("Kiểm tra N có chia hết cho 3 không", "Dùng if N % 3 == 0", "9", "CHIA HET"),
                ("Kiểm tra một người đủ tuổi vị thành niên không", "Dùng if tuoi >= 18", "16", "CHUA DU TUOI"),
                ("Kiểm tra điểm kiểm tra đạt yêu cầu không (>= 5)", "Dùng if diem >= 5", "7", "DAT"),
                ("So sánh hai số nguyên bằng nhau hay khác nhau", "Dùng if a == b", "4\n4", "BANG NHAU"),
                ("Kiểm tra số N có lớn hơn 100 không", "Dùng if N > 100", "120", "LON HON"),
                ("Kiểm tra nhiệt độ nước có sôi không (>= 100 độ C)", "Dùng if t >= 100", "100", "SOI"),
                ("Kiểm tra số nguyên có đúng 1 chữ số không", "Dùng 0 <= N <= 9", "7", "DUNG"),
                ("Kiểm tra mật khẩu đơn giản", "So sánh chuỗi pass == '123'", "123", "DUNG MAT KHAU"),
                ("Kiểm tra ký tự nhập vào có phải dấu cách không", "Dùng ch == ' '", " ", "DAU CACH")
            ],
            "Thông hiểu": [
                ("Tìm số lớn nhất trong 3 số thực a, b, c", "Gán max_val = a rồi so sánh", "4\n9\n2", "9.0"),
                ("Tìm số nhỏ nhất trong 3 số thực a, b, c", "Gán min_val = a rồi so sánh", "4\n9\n2", "2.0"),
                ("Xếp loại học lực theo điểm trung bình", "Dùng if - elif - else", "8.5", "Gioi"),
                ("Kiểm tra 3 cạnh có lập thành tam giác không", "a+b>c và a+c>b và b+c>a", "3\n4\n5", "LA TAM GIAC"),
                ("Kiểm tra năm nhuận dương lịch", "Chia hết 400 hoặc chia hết 4 nhưng không chia hết 100", "2024", "NAM NHUAN"),
                ("Xác định mùa dựa vào số tháng", "Tháng 1-3 Xuân, 4-6 Hạ, 7-9 Thu, 10-12 Đông", "4", "Mua Ha"),
                ("Kiểm tra số chia hết cho cả 3 và 5", "Dùng n % 15 == 0", "30", "CHIA HET"),
                ("Xác định số ngày trong tháng của năm thường", "Tháng 2 có 28 ngày", "2", "28 ngay"),
                ("Giải phương trình bậc nhất ax + b = 0", "Xét a == 0 và a != 0", "2\n-4", "x = 2.0"),
                ("Kiểm tra số có chia hết cho 2 hoặc 3", "Dùng toán tử or", "4", "CO"),
                ("Xác định điểm thi đạt loại Đạt hay Không Đạt", "Toán >= 5 và Văn >= 5", "6\n4", "KHONG DAT"),
                ("Kiểm tra số N có nằm trong đoạn [10, 50] không", "Dùng 10 <= N <= 50", "25", "TRONG DOAN"),
                ("Kiểm tra số N chia 3 dư bao nhiêu", "In N % 3", "8", "Du 2"),
                ("Tìm số ở giữa trong 3 số khác nhau", "Loại bỏ max và min", "3\n7\n5", "5"),
                ("Kiểm tra ký tự nhập vào là chữ in hoa hay in thường", "Dùng isupper()", "A", "HOA")
            ],
            "Vận dụng": [
                ("Phân loại tam giác đều, vuông hay thường", "Dùng Pythagoras và so sánh bằng", "3\n4\n5", "Tam giac vuong"),
                ("Tính giá cước taxi theo các mức kilômét", "Tính tiền lũy tiến bậc thang", "12", "145000"),
                ("Tính tiền điện sinh hoạt bậc thang", "Nhân giá theo từng khung mức", "65", "115000"),
                ("Giải phương trình bậc hai ax^2 + bx + c = 0", "Tính delta = b**2 - 4*a*c", "1\n-3\n2", "x1 = 2.0, x2 = 1.0"),
                ("Xác định tọa độ thuộc góc phần tư thứ mấy", "Kiểm tra dấu x, y", "3\n-2", "Goc phan tu 4"),
                ("Kiểm tra điểm M có nằm trong hình tròn không", "So sánh x^2 + y^2 với R^2", "1\n1\n3", "TRONG HINH TRON"),
                ("Tính tiền vé xem phim theo độ tuổi và ngày trong tuần", "Giảm giá học sinh cuối tuần", "15\n7", "60000"),
                ("Kiểm tra tính hợp lệ của bộ ngày tháng năm", "Kiểm tra số ngày tối đa theo tháng", "31\n4\n2024", "KHONG HOP LE"),
                ("Tìm ngày tiếp theo của ngày D/M/Y", "Tăng ngày, chuyển tháng nếu vượt quá", "28\n2\n2024", "29/2/2024"),
                ("Xác định quý trong năm của một tháng", "Quý 1 đến Quý 4", "11", "Quy 4"),
                ("Kiểm tra chữ số hàng chục gấp đôi hàng đơn vị", "Kiểm tra (n//10) == 2*(n%10)", "42", "DUNG"),
                ("Tính số tiền chiết khấu theo hóa đơn mua hàng", "Hóa đơn > 500k giảm 10%", "600000", "540000"),
                ("Kiểm tra điểm thuộc góc phần tư hay trên trục tọa độ", "Xét x == 0 hoặc y == 0", "0\n5", "TREN TRUC OY"),
                ("Phân loại tam giác tù hay tam giác nhọn", "So sánh a^2 + b^2 với c^2", "4\n5\n7", "Tam giac tu"),
                ("Tính tiền gửi xe theo giờ và loại xe", "Ô tô khác xe máy", "xe_may\n4", "12000")
            ],
            "Vận dụng cao": [
                ("Kiểm tra 4 điểm có tạo thành hình chữ nhật không", "Kiểm tra các đường chéo và vuông góc", "0 0 0 2 3 2 3 0", "HINH CHU NHAT"),
                ("Tìm giao điểm của hai đoạn thẳng trên trục số", "max(a1, a2) đến min(b1, b2)", "1 5 3 7", "[3, 5]"),
                ("Xác định thứ trong tuần theo công thức Zeller", "Tính ngày chính xác theo lịch", "10 9 2026", "Thu Nam"),
                ("Tính tiền phạt quá hạn theo số ngày lũy tiến", "Phạt tăng gấp đôi sau mỗi tuần", "10", "45000"),
                ("Kiểm tra hai hình chữ nhật có giao nhau không", "So sánh tọa độ góc", "0 0 4 4 2 2 6 6", "GIAO NHAU"),
                ("Xác định trạng thái đèn giao thông sau T giây", "Chu kỳ Đỏ - Vàng - Xanh", "45", "DEN XANH"),
                ("Giải hệ phương trình bậc nhất 2 ẩn bằng định thức Cramer", "D = a1*b2 - a2*b1", "1 1 5 2 -1 1", "x = 2.0, y = 3.0"),
                ("Kiểm tra vị trí tương đối của hai đường tròn", "So sánh khoảng cách tâm d với R1+R2", "0 0 3 5 0 2", "TIEP XUC"),
                ("Đổi điểm hệ 10 sang thang điểm chữ (A, B, C, D, F)", "Thang điểm chuẩn tín chỉ", "8.7", "A"),
                ("Kiểm tra năm can chi tương ứng năm dương lịch", "Tính Can và Chi theo số dư", "2026", "Binh Ngo"),
                ("Tính tiền cước bưu phẩm theo trọng lượng và vùng", "Vùng xa phụ thu 20%", "500 2", "36000"),
                ("Bài toán con cờ vua: Kiểm tra quân xe có ăn được không", "Cùng hàng hoặc cùng cột", "1 1 1 8", "AN DUOC"),
                ("Bài toán quân mã cờ vua: Kiểm tra nước đi hợp lệ", "Khoảng cách abs(dx*dy) == 2", "1 1 2 3", "HOP LE"),
                ("Bài toán quân tượng cờ vua: Kiểm tra nước đi hợp lệ", "Đường chéo abs(x1-x2) == abs(y1-y2)", "2 2 5 5", "HOP LE"),
                ("Kiểm tra một điểm có nằm trong tam giác không", "Dùng phương pháp diện tích con", "0 0 4 0 0 4 1 1", "TRONG TAM GIAC")
            ]
        },
        "c3": {
            "Nhận biết": [
                ("In các số từ 1 đến N trên cùng một dòng", "Dùng for i in range(1, N+1)", "5", "1 2 3 4 5"),
                ("In các số từ N về 1", "Dùng range(N, 0, -1)", "4", "4 3 2 1"),
                ("In các số chẵn từ 2 đến 2*N", "Dùng range(2, 2*N+1, 2)", "3", "2 4 6"),
                ("In các số lẻ từ 1 đến 2*N-1", "Dùng range(1, 2*N, 2)", "3", "1 3 5"),
                ("In bảng cửu chương của số K", "Lặp 1 đến 10", "5", "5x1=5 ... 5x10=50"),
                ("In N lần dòng chữ 'Python'", "Lặp N lần print", "3", "Python\nPython\nPython"),
                ("Tính tổng các số từ 1 đến N", "Dùng tong += i", "5", "15"),
                ("Tính tích các số từ 1 đến N (N giai thừa)", "Dùng tich *= i", "4", "24"),
                ("Đếm số chia hết cho 3 trong khoảng [1, N]", "Kiểm tra i % 3 == 0", "10", "3"),
                ("In ra các ước số của số nguyên dương N", "Kiểm tra N % i == 0", "6", "1 2 3 6"),
                ("Đếm số lượng ước số của N", "Tăng biến đếm khi chia hết", "6", "4"),
                ("In N dấu sao (*) trên một dòng", "print('*' * N)", "4", "****"),
                ("Tính tổng các số lẻ từ 1 đến N", "Duyệt bước nhảy 2", "5", "9"),
                ("Tính tổng các số chẵn từ 1 đến N", "Duyệt chẵn cộng dồn", "6", "12"),
                ("In dãy bình phương từ 1 đến N", "In i*i", "4", "1 4 9 16")
            ],
            "Thông hiểu": [
                ("Kiểm tra số nguyên dương N có phải số nguyên tố không", "Đếm ước từ 2 đến căn N", "7", "YES"),
                ("Tìm ước chung lớn nhất UCLN của 2 số", "Dùng thuật toán Euclid", "12\n18", "6"),
                ("Tìm bội chung nhỏ nhất BCNN của 2 số", "BCNN = (a*b)//UCLN", "4\n6", "12"),
                ("Đếm số chữ số của một số nguyên dương N", "Dùng while N > 0: N //= 10", "12345", "5"),
                ("Tính tổng các chữ số của số nguyên N", "Dùng while cộng N % 10", "456", "15"),
                ("Tìm chữ số lớn nhất của số nguyên N", "Tách từng chữ số so sánh", "382", "8"),
                ("Tìm chữ số nhỏ nhất của số nguyên N", "Tách từng chữ số so sánh", "382", "2"),
                ("Tính tổng nghịch đảo S = 1 + 1/2 + ... + 1/N", "Cộng dồn số thực", "2", "1.5"),
                ("In hình chữ nhật đặc kích thước M x N bằng dấu *", "Hai vòng lặp lồng nhau", "2\n3", "***\n***"),
                ("In tam giác vuông sao kích thước N", "Hàng i in i dấu sao", "3", "*\n**\n***"),
                ("Đảo ngược các chữ số của số nguyên N", "Dùng phép nhân 10 cộng dư", "123", "321"),
                ("Kiểm tra số đối xứng (Palindrome)", "So sánh số đảo với số gốc", "121", "YES"),
                ("Tìm số Fibonacci thứ N", "Dùng 2 biến cập nhật liên tiếp", "6", "8"),
                ("In tất cả số chính phương nhỏ hơn hoặc bằng N", "Duyệt i*i <= N", "20", "1 4 9 16"),
                ("Tính tổng giai thừa S = 1! + 2! + ... + N!", "Cộng dồn giai thừa", "3", "9")
            ],
            "Vận dụng": [
                ("In tất cả các số nguyên tố trong đoạn [2, N]", "Lồng vòng lặp kiểm tra nguyên tố", "10", "2 3 5 7"),
                ("Kiểm tra số hoàn hảo (tổng ước bằng chính nó)", "Tổng ước thực sự", "6", "YES"),
                ("Đổi số nguyên N từ hệ thập phân sang nhị phân", "Chia 2 lấy dư liên tiếp", "13", "1101"),
                ("Tìm chữ số đầu tiên của số nguyên dương N", "Lặp while n >= 10: n //= 10", "923", "9"),
                ("In hình chữ nhật rỗng M x N", "Chỉ in viền ngoài", "3\n4", "****\n*  *\n****"),
                ("In tam giác số tăng dần", "In số theo hàng", "3", "1\n1 2\n1 2 3"),
                ("Tìm số nguyên k nhỏ nhất sao cho 1 + 2 + ... + k > N", "Dùng while tong <= N", "10", "5"),
                ("Tính tổng các ước số nguyên tố của N", "Phân tích thừa số nguyên tố", "12", "5"),
                ("Phân tích một số nguyên ra thừa số nguyên tố", "Chia dần cho các ước số nguyên tố", "12", "2 2 3"),
                ("Đếm số lượng số chính phương trong đoạn [A, B]", "Đếm nghiệm căn", "4\n20", "3"),
                ("Kiểm tra số Armstrong bậc 3 (tổng lập phương chữ số bằng chính nó)", "153 = 1^3 + 5^3 + 3^3", "153", "YES"),
                ("Tính tổng S = 1*2 + 2*3 + ... + N*(N+1)", "Cộng dồn tích liên tiếp", "3", "20"),
                ("In tháp số kim tự tháp đối xứng", "Căn lề khoảng trắng", "3", "  1  \n 121 \n12321"),
                ("Mô phỏng trò chơi đoán số nguyên ngẫu nhiên", "Gợi ý Lớn hơn/Nhỏ hơn", "50\n75", "LON HON"),
                ("Tính xấp xỉ số pi theo chuỗi Leibniz", "4 * (1 - 1/3 + 1/5 - 1/7...)", "1000", "3.14")
            ],
            "Vận dụng cao": [
                ("Tìm ước nguyên tố lớn nhất của số nguyên N", "Chia triệt để và lấy ước cuối", "84", "7"),
                ("Tìm số nguyên tố đối xứng nhỏ nhất lớn hơn N", "Kiểm tra đồng thời 2 điều kiện", "100", "101"),
                ("Tính tổng tất cả các chữ số của 2^N", "Lũy thừa lớn và tính tổng chữ số", "15", "26"),
                ("Đếm số số 0 tận cùng của N giai thừa (N!)", "Đếm số lần xuất hiện thừa số 5", "25", "6"),
                ("Tìm số đảo ngược lớn nhất tạo được từ các hoán vị", "Sắp xếp chữ số giảm dần", "315", "531"),
                ("Bài toán Collatz: Đếm số bước đưa N về 1", "N chẵn n/2, N lẻ 3n+1", "6", "8"),
                ("In tam giác Pascal bậc N", "Tính hệ số tổ hợp bằng vòng lặp", "4", "1\n1 1\n1 2 1\n1 3 3 1"),
                ("Tìm chữ số khác 0 cuối cùng của N giai thừa", "Loại bỏ thừa số 10", "5", "2"),
                ("Tính tổng các số tự nhiên nhỏ hơn N chia hết cho 3 hoặc 5", "Công thức số học tối ưu", "10", "23"),
                ("Tìm cặp số bạn bè (amicable numbers) nhỏ hơn N", "Tổng ước số này bằng số kia", "300", "220 284"),
                ("Giải bài toán cổ: Vừa gà vừa chó 36 con 100 chân", "Vét cạn nghiệm gà và chó", "36\n100", "22 con ga, 14 con cho"),
                ("Tìm số nguyên nhỏ nhất chia hết cho tất cả từ 1 đến N", "BCNN liên tiếp", "5", "60"),
                ("In xoắn ốc ma trận số kích thước N x N", "Vòng lặp 4 hướng", "3", "1 2 3\n8 9 4\n7 6 5"),
                ("Tính căn bậc hai theo phương pháp Newton-Raphson", "Lặp x = (x + N/x)/2", "9", "3.0"),
                ("Đếm số nghiệm nguyên dương của phương trình x + y + z = N", "3 vòng lặp lồng có điều kiện", "5", "6")
            ]
        },
        "c4": {
            "Nhận biết": [
                ("Khởi tạo và in các phần tử trong danh sách", "Dùng print(*A)", "3\n1 2 3", "1 2 3"),
                ("In độ dài của danh sách N phần tử", "Dùng len(A)", "4\n1 5 9 2", "4"),
                ("In phần tử đầu tiên của danh sách", "In A[0]", "3\n7 8 9", "7"),
                ("In phần tử cuối cùng của danh sách", "In A[-1]", "3\n7 8 9", "9"),
                ("Tính tổng các phần tử trong danh sách", "Dùng sum(A)", "3\n1 2 3", "6"),
                ("Tìm phần tử lớn nhất trong danh sách", "Dùng max(A)", "4\n3 9 1 4", "9"),
                ("Tìm phần tử nhỏ nhất trong danh sách", "Dùng min(A)", "4\n3 9 1 4", "1"),
                ("Đếm số lần xuất hiện của số X trong mảng", "Dùng A.count(X)", "4\n1 2 2 3\n2", "2"),
                ("Thêm phần tử X vào cuối danh sách", "Dùng A.append(X)", "3\n1 2 3\n4", "1 2 3 4"),
                ("Xóa phần tử đầu tiên có giá trị X", "Dùng A.remove(X)", "3\n1 2 3\n2", "1 3"),
                ("In danh sách theo thứ tự đảo ngược", "Dùng A[::-1]", "3\n1 2 3", "3 2 1"),
                ("Sắp xếp danh sách theo thứ tự tăng dần", "Dùng sorted(A)", "4\n5 2 8 1", "1 2 5 8"),
                ("Sắp xếp danh sách theo thứ tự giảm dần", "Dùng sorted(A, reverse=True)", "4\n5 2 8 1", "8 5 2 1"),
                ("Kiểm tra giá trị X có nằm trong danh sách không", "Dùng X in A", "3\n1 2 3\n2", "YES"),
                ("Tạo danh sách gồm N số 0", "Dùng [0] * N", "3", "0 0 0")
            ],
            "Thông hiểu": [
                ("Tính trung bình cộng các phần tử trong danh sách", "sum(A) / len(A)", "4\n2 4 6 8", "5.0"),
                ("Đếm số lượng số chẵn trong danh sách", "Đếm x % 2 == 0", "5\n1 2 3 4 5", "2"),
                ("Đếm số lượng số lẻ trong danh sách", "Đếm x % 2 != 0", "5\n1 2 3 4 5", "3"),
                ("Tính tổng các số dương trong danh sách", "Cộng x nếu x > 0", "4\n-2 3 -1 5", "8"),
                ("Tính tổng các số âm trong danh sách", "Cộng x nếu x < 0", "4\n-2 3 -1 5", "-3"),
                ("Tìm vị trí chỉ số đầu tiên của phần tử X", "Dùng A.index(X)", "4\n10 20 30 40\n30", "2"),
                ("Tách mảng thành hai danh sách chẵn và lẻ", "Lọc vào 2 list con", "4\n1 2 3 4", "Chan: 2 4 | Le: 1 3"),
                ("Nhân đôi tất cả các phần tử trong danh sách", "Dùng [x*2 for x in A]", "3\n1 2 3", "2 4 6"),
                ("Thay thế tất cả số âm bằng số 0", "Dùng [x if x>=0 else 0 for x in A]", "4\n-1 2 -3 4", "0 2 0 4"),
                ("Tìm phần tử lớn thứ nhì trong danh sách", "Sắp xếp giảm dần và lấy phần tử kế tiếp", "4\n10 20 5 15", "15"),
                ("In các phần tử nằm ở vị trí chỉ số chẵn", "Duyệt range(0, len(A), 2)", "4\n10 20 30 40", "10 30"),
                ("Tính tích các phần tử khác 0 trong danh sách", "Lặp bỏ qua số 0", "4\n2 0 3 4", "24"),
                ("Kiểm tra mảng có tăng dần nghiêm ngặt không", "So sánh A[i] < A[i+1]", "3\n1 2 3", "YES"),
                ("Nối hai danh sách A và B thành một danh sách", "Dùng A + B", "2\n1 2\n3 4", "1 2 3 4"),
                ("Xóa phần tử tại chỉ số K trong mảng", "Dùng del A[K]", "4\n10 20 30 40\n1", "10 30 40")
            ],
            "Vận dụng": [
                ("Loại bỏ các phần tử trùng lặp, giữ lại phần tử duy nhất", "Duyệt thêm mới hoặc dùng set", "5\n1 2 2 3 1", "1 2 3"),
                ("Đếm số lượng số nguyên tố có trong danh sách", "Viết hàm kiểm tra cho từng x", "5\n2 3 4 5 6", "3"),
                ("Chèn số X vào mảng đã sắp xếp sao cho vẫn giữ thứ tự tăng", "Tìm vị trí và insert", "3\n1 3 5\n4", "1 3 4 5"),
                ("Tìm phần tử xuất hiện nhiều lần nhất trong mảng", "Đếm tần suất", "6\n1 2 2 3 2 4", "2"),
                ("Dịch chuyển vòng quanh các phần tử sang phải 1 vị trí", "A[-1:] + A[:-1]", "3\n1 2 3", "3 1 2"),
                ("Tính trung bình cộng các số lớn hơn trung bình cộng cả mảng", "Lọc 2 lần", "4\n1 2 5 8", "6.5"),
                ("Tìm khoảng cách lớn nhất giữa hai phần tử bất kỳ", "max(A) - min(A)", "4\n2 9 1 5", "8"),
                ("Gộp hai mảng đã sắp xếp tăng dần thành một mảng tăng dần", "Kỹ thuật 2 con trỏ", "2\n1 4\n2 3", "1 2 3 4"),
                ("Tách số âm về đầu mảng, số dương về cuối mảng", "Lọc nối danh sách", "4\n3 -1 2 -4", "-1 -4 3 2"),
                ("Đếm số cặp phần tử liền kề có tích là số chẵn", "Kiểm tra A[i]*A[i+1]%2 == 0", "3\n1 2 3", "2"),
                ("Tìm cặp số trong mảng có tổng bằng số K cho trước", "Duyệt tìm A[i]+A[j] == K", "4\n1 4 2 3\n5", "1 4"),
                ("Tính tổng các phần tử là số chính phương", "Cộng dồn số chính phương", "4\n4 5 9 10", "13"),
                ("Đảo ngược từng nửa của danh sách chẵn phần tử", "Cắt lát 2 nửa đảo ngược", "4\n1 2 3 4", "2 1 4 3"),
                ("Tìm giá trị dương nhỏ nhất trong mảng", "Lọc x > 0 rồi min", "4\n-3 5 2 -1", "2"),
                ("Kiểm tra danh sách có đối xứng không", "A == A[::-1]", "3\n1 2 1", "YES")
            ],
            "Vận dụng cao": [
                ("Tìm dãy con liên tiếp có tổng lớn nhất (Thuật toán Kadane)", "Theo dõi max_ending_here", "5\n-2 1 -3 4 -1", "4"),
                ("Tìm số còn thiếu trong dãy hoán vị từ 1 đến N", "Tổng lý thuyết trừ tổng thực tế", "4\n1 2 4 5", "3"),
                ("Đếm số lượng cặp nghịch thế trong mảng (i < j và A[i] > A[j])", "Vét cạn hoặc Merge Sort", "3\n3 1 2", "2"),
                ("Dồn tất cả các số 0 về cuối mảng mà không đổi thứ tự số khác", "Dùng 2 con trỏ in-place", "4\n0 1 0 3", "1 3 0 0"),
                ("Tìm phần tử chiếm đa số (xuất hiện > N/2 lần)", "Thuật toán Boyer-Moore", "5\n2 2 1 2 3", "2"),
                ("Tìm độ dài dãy con tăng liên tiếp dài nhất", "Theo dõi biến đếm độ dài", "5\n1 2 2 3 4", "3"),
                ("Sắp xếp mảng số theo tần suất xuất hiện giảm dần", "Custom sort theo count", "5\n1 2 2 3 3", "2 2 3 3 1"),
                ("Tìm 3 số trong mảng có tích lớn nhất", "max(A[-1]*A[-2]*A[-3], A[0]*A[1]*A[-1])", "4\n-10 -10 5 2", "500"),
                ("Chia danh sách thành K phần đều nhau nhất có thể", "Chia mảng con", "5\n1 2 3 4 5\n2", "[[1, 2, 3], [4, 5]]"),
                ("Xoay danh sách sang trái K vị trí", "A[K:] + A[:K]", "4\n1 2 3 4\n2", "3 4 1 2"),
                ("Tìm khoảng cách nhỏ nhất giữa hai phần tử bất kỳ", "Sort rồi so sánh liền kề", "4\n1 5 3 19", "2"),
                ("Tìm số lặp lại đầu tiên trong danh sách", "Dùng set lưu vết", "4\n2 1 3 1", "1"),
                ("Tính tổng các mảng con kích thước K (Sliding Window)", "Cửa sổ trượt", "4\n1 2 3 4\n2", "3 5 7"),
                ("Kiểm tra một mảng có phải là tập con của mảng khác không", "Dùng set.issubset", "4\n1 2 3 4\n2 3", "YES"),
                ("Tìm phần tử đạt giá trị đỉnh (lớn hơn hai phần tử lân cận)", "So sánh A[i-1] < A[i] > A[i+1]", "5\n1 3 20 4 1", "20")
            ]
        },
        "c5": {
            "Nhận biết": [
                ("Viết hàm tính lập phương của một số n", "def lap_phuong(n): return n**3", "3", "27"),
                ("Viết hàm tính chu vi hình tròn", "def chu_vi(r): return 2*3.14*r", "5", "31.4"),
                ("Viết hàm tính diện tích hình chữ nhật", "def dt(a, b): return a*b", "4\n5", "20"),
                ("In độ dài của một xâu ký tự", "len(s)", "Python", "6"),
                ("Chuyển toàn bộ xâu sang chữ in hoa", "s.upper()", "tin hoc", "TIN HOC"),
                ("Chuyển toàn bộ xâu sang chữ in thường", "s.lower()", "TIN HOC", "tin hoc"),
                ("Đếm số lần xuất hiện của ký tự C trong xâu S", "s.count(C)", "hello\nl", "2"),
                ("Nối hai chuỗi ký tự với nhau", "s1 + s2", "Xin\nChao", "XinChao"),
                ("Viết hàm kiểm tra số dương", "return n > 0", "5", "True"),
                ("Viết hàm kiểm tra số chẵn", "return n % 2 == 0", "4", "True"),
                ("Đảo ngược một xâu ký tự", "s[::-1]", "abcd", "dcba"),
                ("In ký tự đầu tiên và cuối cùng của chuỗi", "s[0] và s[-1]", "Python", "P n"),
                ("Thay thế khoảng trắng bằng dấu gạch dưới trong xâu", "s.replace(' ', '_')", "hoc python", "hoc_python"),
                ("Viết hàm tìm giá trị tuyệt đối của số x", "def tuyet_doi(x): return abs(x)", "-15", "15"),
                ("Viết hàm in lời chào theo tên", "def chao(ten): return 'Chao ' + ten", "Nam", "Chao Nam")
            ],
            "Thông hiểu": [
                ("Viết hàm kiểm tra số nguyên tố kiem_tra_snt(n)", "Trả về True nếu là số nguyên tố", "7", "True"),
                ("Viết hàm tìm UCLN ucln(a, b) theo thuật toán Euclid", "while b: a, b = b, a % b", "12\n18", "6"),
                ("Đếm số lượng từ trong một câu văn bản", "len(s.split())", "Chuc cac em hoc tot", "5"),
                ("Đếm số lượng chữ số có trong xâu", "Đếm c.isdigit()", "Edu10Coder2026", "6"),
                ("Đếm số lượng chữ cái in hoa trong xâu", "Đếm c.isupper()", "TinHoc10", "3"),
                ("Chuẩn hóa xâu: Viết hoa chữ cái đầu mỗi từ", "s.title()", "nguyen van an", "Nguyen Van An"),
                ("Xóa bỏ khoảng trắng thừa ở hai đầu xâu", "s.strip()", "   hello   ", "hello"),
                ("Kiểm tra xâu có đối xứng không (Palindrome string)", "s == s[::-1]", "radar", "YES"),
                ("Viết hàm tính giai thừa giai_thua(n)", "Dùng vòng lặp trong hàm", "5", "120"),
                ("Viết hàm tính tổng ước số tong_uoc(n)", "Lặp từ 1 đến n", "6", "12"),
                ("Kiểm tra xâu ký tự chỉ chứa chữ số", "s.isdigit()", "12345", "True"),
                ("Viết hàm giải phương trình ax + b = 0", "Trả về chuỗi nghiệm", "2\n-4", "2.0"),
                ("Tìm vị trí đầu tiên của từ khóa trong văn bản", "s.find(sub)", "lap trinh python\npython", "10"),
                ("Viết hàm tính lũy thừa luy_thua(a, b)", "return a ** b", "2\n3", "8"),
                ("Đếm số nguyên âm tiếng Anh trong câu", "Duyệt c in 'aeiouAEIOU'", "computer", "3")
            ],
            "Vận dụng": [
                ("Viết hàm chuẩn hóa họ tên chuẩn GDPT", "Tách từ, capitalize và nối lại", "  nguyen   thi   hoa  ", "Nguyen Thi Hoa"),
                ("Xóa tất cả các chữ số xuất hiện trong xâu ký tự", "Lọc not c.isdigit()", "Tin10Hoc2026", "TinHoc"),
                ("Nén xâu ký tự cơ bản: đếm ký tự liên tiếp", "Run-length encoding", "aaabbc", "a3b2c1"),
                ("Viết hàm kiem_tra_hoan_hao(n)", "Tổng ước thực sự == n", "28", "True"),
                ("Đếm tần suất xuất hiện của mỗi ký tự trong xâu", "Dùng dictionary", "hello", "h:1 e:1 l:2 o:1"),
                ("Mã hóa Caesar đơn giản (dịch k vị trí)", "Dùng ord() và chr()", "abc\n1", "bcd"),
                ("Tách phần tên và phần họ đệm từ họ tên đầy đủ", "Tách từ cuối cùng làm tên", "Nguyen Van An", "Ho dem: Nguyen Van | Ten: An"),
                ("Kiểm tra mật khẩu mạnh (>= 8 ký tự, có hoa, thường, số)", "Kiểm tra 4 tiêu chí", "Pass1234", "MANH"),
                ("Viết hàm rut_gon_phan_so(a, b)", "Chia cho UCLN", "6\n8", "3/4"),
                ("Tìm từ dài nhất trong một đoạn văn", "max(s.split(), key=len)", "Lap trinh Python co ban", "Python"),
                ("Viết hàm fibonacci(n) trả về số Fib thứ n", "Quy hoạch động hoặc lặp", "7", "13"),
                ("Chuyển chuỗi nhị phân sang số nguyên thập phân", "int(s, 2)", "1101", "13"),
                ("Đảo ngược thứ tự các từ trong câu văn", "' '.join(s.split()[::-1])", "I love Python", "Python love I"),
                ("Kiểm tra hai xâu có phải đảo chữ của nhau (Anagram)", "sorted(s1) == sorted(s2)", "listen\nsilent", "YES"),
                ("Xóa các ký tự đặc biệt chỉ giữ chữ cái và số", "c.isalnum()", "he@llo#2026!", "hello2026")
            ],
            "Vận dụng cao": [
                ("Viết hàm đệ quy tính tháp Hà Nội (Tower of Hanoi)", "Quy luật 3 cọc", "3", "7 buoc"),
                ("Tính biểu thức số học đơn giản dạng chuỗi (eval an toàn)", "Xử lý cộng trừ đơn giản", "12 + 8", "20"),
                ("Mã hóa và giải mã số La Mã sang số nguyên", "Bảng tra chữ số La Mã", "XIV", "14"),
                ("Tìm xâu con chung dài nhất giữa hai chuỗi ký tự", "Quy hoạch động chuỗi", "AGGTAB\nGXTXAYB", "GTAB"),
                ("Viết hàm đệ quy ucln_de_quy(a, b)", "ucln(b, a%b) nếu b else a", "24\n36", "12"),
                ("Kiểm tra biểu thức đóng mở ngoặc hợp lệ", "Dùng cấu trúc ngăn xếp Stack", "(())()", "DUNG"),
                ("Tìm từ xuất hiện nhiều nhất trong văn bản", "Đếm tần suất từ", "hoc hoc nua hoc mai", "hoc"),
                ("Sinh tất cả các hoán vị của một chuỗi ký tự", "Đệ quy hoán vị", "ab", "ab ba"),
                ("Viết hàm sắp xếp danh sách học sinh theo điểm giảm dần", "lambda x: x['diem']", "Nam 8.5, An 9.0", "An: 9.0, Nam: 8.5"),
                ("Tách trích xuất tất cả các địa chỉ email có trong văn bản", "Regex tìm kiếm pattern", "Lien he: gv@edu.vn hoac admin@test.com", "gv@edu.vn admin@test.com"),
                ("Chuẩn hóa văn bản: Chấm câu viết hoa và cách 1 space", "Xử lý dấu câu", "chao em.hoc bai di.", "Chao em. Hoc bai di."),
                ("Viết hàm tính khoảng cách Levenshtein giữa 2 xâu", "Khoảng cách chỉnh sửa tối thiểu", "kitten\nsitting", "3"),
                ("Giải mã mật mã xâu đảo ngược từ", "Đảo ngược từng từ giữ nguyên vị trí", "olleH dlroW", "Hello World"),
                ("Tìm xâu con đối xứng dài nhất trong xâu S", "Mở rộng từ tâm", "babad", "bab"),
                ("Viết hàm tính giai thừa của số cực lớn chính xác tuyệt đối", "Hỗ trợ số nguyên lớn Python", "20", "2432902008176640000")
            ]
        }
    }

    for ch_idx, ch_key in enumerate(["c1", "c2", "c3", "c4", "c5"], 1):
        for lvl_idx, lvl_name in enumerate(levels):
            prob_list = bank[ch_key][lvl_name]
            for i, p in enumerate(prob_list):
                ex_num = lvl_idx * 15 + i + 1
                ex_code = f"C{ch_idx}_{ex_num:02d}"
                test_cases = [
                    {"input": p[2], "output": p[3]},
                    {"input": p[2], "output": p[3]}
                ]
                exercises[ch_key].append({
                    "code": ex_code,
                    "title": p[0],
                    "level": lvl_name,
                    "chapter": CHAPTER_NAMES[ch_key],
                    "problem": f"Đề bài bài tập {ex_code}: {p[0]}. Học sinh hãy viết chương trình Python nhận dữ liệu chuẩn từ bàn phím và in kết quả chính xác ra màn hình.",
                    "hint": p[1],
                    "testcases_json": json.dumps(test_cases)
                })
    return exercises

CURRICULUM_EXERCISES = _build_curriculum_exercises()