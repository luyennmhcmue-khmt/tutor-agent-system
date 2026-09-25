def get_c1_exercises():
    data = [
        # --- 10 bài Nhận biết (C1_01 -> C1_10) ---
        ("C1_01", "Nhận biết", "In dòng chữ xin chào", "Viết chương trình in ra màn hình chính xác dòng chữ: `Xin chào Python!`", "print('Xin chào Python!')", "Lệnh print() cơ bản", "", "Xin chào Python!"),
        ("C1_02", "Nhận biết", "In họ và tên học sinh", "Nhập họ tên từ bàn phím và in lại chính xác họ tên đó.", "ten = input()\nprint(ten)", "Hàm input() đọc chuỗi", "Nguyen Van An", "Nguyen Van An"),
        ("C1_03", "Nhận biết", "In số nguyên vừa nhập", "Nhập một số nguyên n từ bàn phím và in số đó ra màn hình.", "n = int(input())\nprint(n)", "Ép kiểu int()", "100", "100"),
        ("C1_04", "Nhận biết", "In số thực vừa nhập", "Nhập một số thực x từ bàn phím và in số đó ra màn hình.", "x = float(input())\nprint(x)", "Ép kiểu float()", "3.14", "3.14"),
        ("C1_05", "Nhận biết", "Phép cộng số nguyên", "Tính và in ra giá trị của biểu thức 15 + 25.", "print(15 + 25)", "Toán tử cộng +", "", "40"),
        ("C1_06", "Nhận biết", "Phép trừ số nguyên", "Tính và in ra giá trị của biểu thức 100 - 37.", "print(100 - 37)", "Toán tử trừ -", "", "63"),
        ("C1_07", "Nhận biết", "Phép nhân số nguyên", "Tính và in ra giá trị của biểu thức 12 * 8.", "print(12 * 8)", "Toán tử nhân *", "", "96"),
        ("C1_08", "Nhận biết", "Phép chia lấy phần nguyên", "Tính và in ra phần nguyên của phép chia 17 cho 5.", "print(17 // 5)", "Toán tử chia nguyên //", "", "3"),
        ("C1_09", "Nhận biết", "Phép chia lấy phần dư", "Tính và in ra phần dư của phép chia 17 cho 5.", "print(17 % 5)", "Toán tử chia dư %", "", "2"),
        ("C1_10", "Nhận biết", "In với tham số sep", "In 3 số 1, 2, 3 trên một dòng phân cách nhau bởi dấu gạch ngang `-`.", "print(1, 2, 3, sep='-')", "Tham số sep trong print", "", "1-2-3"),

        # --- 10 bài Thông hiểu (C1_11 -> C1_20) ---
        ("C1_11", "Thông hiểu", "Tính tổng hai số nguyên", "Nhập 2 số nguyên a và b trên 2 dòng. In ra tổng của chúng.", "a = int(input())\nb = int(input())\nprint(a + b)", "Nhập và tính tổng", "5\n7", "12"),
        ("C1_12", "Thông hiểu", "Tính hiệu hai số nguyên", "Nhập 2 số nguyên a và b trên 2 dòng. In ra hiệu a - b.", "a = int(input())\nb = int(input())\nprint(a - b)", "Nhập và tính hiệu", "20\n8", "12"),
        ("C1_13", "Thông hiểu", "Tính tích hai số nguyên", "Nhập 2 số nguyên a và b trên 2 dòng. In ra tích a * b.", "a = int(input())\nb = int(input())\nprint(a * b)", "Nhập và tính tích", "6\n9", "54"),
        ("C1_14", "Thông hiểu", "Tính chu vi hình vuông", "Nhập cạnh hình vuông a (nguyên). In ra chu vi hình vuông.", "a = int(input())\nprint(a * 4)", "Chu vi hình vuông", "5", "20"),
        ("C1_15", "Thông hiểu", "Tính diện tích hình vuông", "Nhập cạnh hình vuông a (nguyên). In ra diện tích hình vuông.", "a = int(input())\nprint(a * a)", "Diện tích hình vuông", "6", "36"),
        ("C1_16", "Thông hiểu", "Tính chu vi hình chữ nhật", "Nhập dài a và rộng b trên 2 dòng (nguyên). In chu vi (a + b) * 2.", "a = int(input())\nb = int(input())\nprint((a + b) * 2)", "Chu vi hình chữ nhật", "4\n5", "18"),
        ("C1_17", "Thông hiểu", "Đổi độ C sang độ F", "Nhập nhiệt độ C (số thực). In độ F = C * 1.8 + 32.", "c = float(input())\nprint(c * 1.8 + 32)", "Công thức đổi nhiệt độ", "0", "32.0"),
        ("C1_18", "Thông hiểu", "Đổi km sang mét", "Nhập khoảng cách km (nguyên). In số mét tương ứng.", "km = int(input())\nprint(km * 1000)", "Chuyển đơn vị độ dài", "5", "5000"),
        ("C1_19", "Thông hiểu", "Tính tiền mua vở", "Dòng 1 số lượng vở, dòng 2 đơn giá mỗi quyển. In tổng tiền.", "sl = int(input())\ngia = int(input())\nprint(sl * gia)", "Toán thực tế số lượng đơn giá", "10\n7000", "70000"),
        ("C1_20", "Thông hiểu", "Chia đều kẹo", "Nhập số kẹo n và số bạn k trên 2 dòng. In số kẹo mỗi bạn nhận được.", "n = int(input())\nk = int(input())\nprint(n // k)", "Phép chia nguyên thực tế", "25\n4", "6"),

        # --- 10 bài Vận dụng (C1_21 -> C1_30) ---
        ("C1_21", "Vận dụng", "Tính diện tích hình chữ nhật", "Nhập chiều dài và chiều rộng số thực trên 2 dòng. In ra diện tích.", "a = float(input())\nb = float(input())\nprint(a * b)", "Diện tích số thực", "4.5\n2.0", "9.0"),
        ("C1_22", "Vận dụng", "Tính diện tích hình thang", "Dòng 1 đáy a, dòng 2 đáy b, dòng 3 chiều cao h. In diện tích (a + b) * h / 2.", "a, b, h = float(input()), float(input()), float(input())\nprint((a + b) * h / 2)", "Hình thang", "3\n5\n4", "16.0"),
        ("C1_23", "Vận dụng", "Tính chỉ số BMI", "Dòng 1 cân nặng (kg), dòng 2 chiều cao (m). In BMI = w / (h*h) làm tròn 1 chữ số.", "w, h = float(input()), float(input())\nprint(round(w / (h * h), 1))", "Chỉ số khối BMI", "50\n1.6", "19.5"),
        ("C1_24", "Vận dụng", "Đổi giờ và phút sang phút", "Dòng 1 số giờ, dòng 2 số phút. In tổng số phút tương ứng.", "h, m = int(input()), int(input())\nprint(h * 60 + m)", "Quy đổi thời gian", "2\n30", "150"),
        ("C1_25", "Vận dụng", "Tính chu vi tam giác", "Nhập 3 cạnh tam giác a, b, c trên 3 dòng. In chu vi tam giác.", "a, b, c = int(input()), int(input()), int(input())\nprint(a + b + c)", "Chu vi tam giác", "3\n4\n5", "12"),
        ("C1_26", "Vận dụng", "Tính trung bình cộng 3 số", "Nhập 3 số nguyên a, b, c trên 3 dòng. In trung bình cộng của chúng.", "a, b, c = int(input()), int(input()), int(input())\nprint((a + b + c) / 3)", "Trung bình cộng", "3\n6\n9", "6.0"),
        ("C1_27", "Vận dụng", "Tính tiền lương theo ngày công", "Dòng 1 số ngày làm, dòng 2 tiền công 1 ngày. In tổng lương.", "c, l = int(input()), int(input())\nprint(c * l)", "Toán thực tế lương công", "22\n300000", "6600000"),
        ("C1_28", "Vận dụng", "Tính vận tốc chuyển động", "Dòng 1 quãng đường s (km), dòng 2 thời gian t (h). In vận tốc v = s / t.", "s, t = float(input()), float(input())\nprint(s / t)", "Vận tốc vật lý", "120\n2", "60.0"),
        ("C1_29", "Vận dụng", "Số kẹo dư sau khi chia", "Nhập số kẹo n và số bạn k. In số kẹo dư không thể chia đều.", "n, k = int(input()), int(input())\nprint(n % k)", "Phép chia dư thực tế", "25\n4", "1"),
        ("C1_30", "Vận dụng", "Tính chu vi đường tròn", "Nhập bán kính r (số thực). In chu vi đường tròn C = 2 * 3.14 * r.", "r = float(input())\nprint(round(2 * 3.14 * r, 2))", "Chu vi đường tròn", "5", "31.4"),

        # --- 10 bài Vận dụng cao (C1_31 -> C1_40) ---
        ("C1_31", "Vận dụng cao", "Đổi giây sang giờ phút giây", "Nhập số giây T. In định dạng: 'h giờ m phút s giây'.", "t = int(input())\nprint(f'{t//3600} giờ {(t%3600)//60} phút {t%60} giây')", "Quy đổi thời gian nâng cao", "3665", "1 giờ 1 phút 5 giây"),
        ("C1_32", "Vận dụng cao", "Tổng chữ số của số 2 chữ số", "Nhập số nguyên N có 2 chữ số. In tổng 2 chữ số đó.", "n = int(input())\nprint(n // 10 + n % 10)", "Tách chữ số số học", "47", "11"),
        ("C1_33", "Vận dụng cao", "Tổng chữ số của số 3 chữ số", "Nhập số nguyên N có 3 chữ số. In tổng 3 chữ số đó.", "n = int(input())\nprint(n // 100 + (n // 10) % 10 + n % 10)", "Tách chữ số hàng trăm", "123", "6"),
        ("C1_34", "Vận dụng cao", "Đảo ngược số có 3 chữ số", "Nhập số nguyên N có 3 chữ số. In ra số đảo ngược.", "n = input().strip()\nprint(n[::-1])", "Xử lý đảo chuỗi số", "358", "853"),
        ("C1_35", "Vận dụng cao", "Khoảng cách trên trục số", "Nhập 2 số thực a và b trên 2 dòng. In khoảng cách |a - b|.", "a, b = float(input()), float(input())\nprint(abs(a - b))", "Hàm abs() trị tuyệt đối", "7.5\n2.5", "5.0"),
        ("C1_36", "Vận dụng cao", "Tính tiền taxi mở cửa", "Nhập số km đi được x. Giá mở cửa 10000đ/km đầu, km tiếp theo 12000đ/km (x >= 1).", "x = int(input())\nprint(10000 + (x - 1) * 12000)", "Bậc thang tính tiền taxi", "5", "58000"),
        ("C1_37", "Vận dụng cao", "Tính số can nước cần chuẩn bị", "Có V lít nước, mỗi can chứa tối đa C lít. Tính số can ít nhất cần có để chứa hết.", "import math\nv, c = int(input()), int(input())\nprint(math.ceil(v / c))", "Hàm làm tròn lên math.ceil", "11\n3", "4"),
        ("C1_38", "Vận dụng cao", "Đổi tiền ATM mệnh giá 500k", "Nhập số tiền n (bội của 1000). Rút được bao nhiêu tờ 500k và số dư còn lại.", "n = int(input())\nprint(f'{n // 500000} to, du {n % 500000}')", "Chia nguyên và dư ATM", "1250000", "2 to, du 250000"),
        ("C1_39", "Vận dụng cao", "Diện tích tam giác Heron", "Nhập 3 cạnh tam giác 3, 4, 5 trên 3 dòng. In diện tích theo công thức Heron.", "import math\na,b,c = float(input()), float(input()), float(input())\np = (a+b+c)/2\nprint(math.sqrt(p*(p-a)*(p-b)*(p-c)))", "Công thức Heron", "3\n4\n5", "6.0"),
        ("C1_40", "Vận dụng cao", "Làm tròn số thực 2 chữ số", "Nhập số thực x. In giá trị làm tròn đến 2 chữ số thập phân.", "x = float(input())\nprint(round(x, 2))", "Hàm round() số thực", "3.14159", "3.14")
    ]
    return [{"id": d[0], "chapter": "Chương 1: Vào/Ra & Biến cơ sở (Bài 16-18)", "difficulty": d[1], "title": d[2], "desc": d[3], "hint": d[4], "concept": d[5], "tests": [{"input": d[6], "expected": d[7]}]} for d in data]

def get_c2_exercises():
    data = [
        # --- 10 bài Nhận biết (C2_01 -> C2_10) ---
        ("C2_01", "Nhận biết", "Kiểm tra số chẵn lẻ", "Nhập số nguyên n. In `CHAN` nếu n chẵn, ngược lại in `LE`.", "n = int(input())\nprint('CHAN' if n % 2 == 0 else 'LE')", "Rẽ nhánh chẵn lẻ", "8", "CHAN"),
        ("C2_02", "Nhận biết", "Kiểm tra số âm hay dương", "Nhập số nguyên n khác 0. In `DUONG` nếu n > 0, ngược lại in `AM`.", "n = int(input())\nprint('DUONG' if n > 0 else 'AM')", "So sánh dấu của số", "15", "DUONG"),
        ("C2_03", "Nhận biết", "Kiểm tra chia hết cho 5", "Nhập n. In `YES` nếu n chia hết cho 5, ngược lại in `NO`.", "n = int(input())\nprint('YES' if n % 5 == 0 else 'NO')", "Toán tử chia dư %", "25", "YES"),
        ("C2_04", "Nhận biết", "Kiểm tra số bằng 0", "Nhập n. In `ZERO` nếu n == 0, ngược lại in `NOT ZERO`.", "n = int(input())\nprint('ZERO' if n == 0 else 'NOT ZERO')", "Toán tử so sánh bằng ==", "0", "ZERO"),
        ("C2_05", "Nhận biết", "In dãy số từ 1 đến 5", "Dùng vòng lặp in các số từ 1 đến 5 trên một dòng cách nhau bởi dấu cách.", "print('1 2 3 4 5')", "Vòng lặp range()", "", "1 2 3 4 5"),
        ("C2_06", "Nhận biết", "In dãy số giảm từ 5 về 1", "In các số từ 5 về 1 cách nhau bởi dấu cách.", "print('5 4 3 2 1')", "Bước nhảy âm trong range", "", "5 4 3 2 1"),
        ("C2_07", "Nhận biết", "In các số chẵn nhỏ hơn 10", "In các số chẵn dương nhỏ hơn 10: 2 4 6 8.", "print('2 4 6 8')", "Dãy số chẵn", "", "2 4 6 8"),
        ("C2_08", "Nhận biết", "Kiểm tra số lớn hơn 100", "Nhập n. In `LON` nếu n > 100, ngược lại in `NHO`.", "n = int(input())\nprint('LON' if n > 100 else 'NHO')", "So sánh ngưỡng", "150", "LON"),
        ("C2_09", "Nhận biết", "In từ lặp 3 lần", "Nhập từ s. In s lặp lại 3 lần cách nhau bằng dấu cách.", "s = input()\nprint(f'{s} {s} {s}')", "Vòng lặp lặp chuỗi", "Python", "Python Python Python"),
        ("C2_10", "Nhận biết", "Kiểm tra đủ tuổi vào lớp 10", "Nhập tuổi t. Nếu t >= 15 in `DU TUOI`, ngược lại in `CHUA DU`.", "t = int(input())\nprint('DU TUOI' if t >= 15 else 'CHUA DU')", "Điều kiện logic >= 15", "15", "DU TUOI"),

        # --- 10 bài Thông hiểu (C2_11 -> C2_20) ---
        ("C2_11", "Thông hiểu", "Tìm số lớn hơn trong 2 số", "Nhập 2 số nguyên a và b trên 2 dòng. In số lớn hơn.", "a, b = int(input()), int(input())\nprint(max(a, b))", "Hàm max 2 số", "12\n25", "25"),
        ("C2_12", "Thông hiểu", "Tìm số nhỏ hơn trong 2 số", "Nhập 2 số nguyên a và b trên 2 dòng. In số nhỏ hơn.", "a, b = int(input()), int(input())\nprint(min(a, b))", "Hàm min 2 số", "12\n25", "12"),
        ("C2_13", "Thông hiểu", "Tính tổng dãy số từ 1 đến N", "Nhập số nguyên dương N. In tổng 1 + 2 + ... + N.", "n = int(input())\nprint(sum(range(1, n + 1)))", "Vòng lặp tích lũy tổng", "5", "15"),
        ("C2_14", "Thông hiểu", "Tính giai thừa của N", "Nhập N (N >= 1). In N! = 1 * 2 * ... * N.", "import math\nprint(math.factorial(int(input())))", "Tính giai thừa", "4", "24"),
        ("C2_15", "Thông hiểu", "Đếm số ước số của N", "Nhập số nguyên N. Đếm xem N có bao nhiêu ước nguyên dương.", "n = int(input())\nprint(sum(1 for i in range(1, n+1) if n % i == 0))", "Duyệt ước số", "6", "4"),
        ("C2_16", "Thông hiểu", "Tính tổng các số chẵn từ 1 đến N", "Nhập N. In tổng các số chẵn trong đoạn [1, N].", "n = int(input())\nprint(sum(i for i in range(2, n+1, 2)))", "Tổng số chẵn", "6", "12"),
        ("C2_17", "Thông hiểu", "Tính tổng các số lẻ từ 1 đến N", "Nhập N. In tổng các số lẻ trong đoạn [1, N].", "n = int(input())\nprint(sum(i for i in range(1, n+1, 2)))", "Tổng số lẻ", "5", "9"),
        ("C2_18", "Thông hiểu", "Đếm số chữ số của N", "Nhập số nguyên dương N. In ra số lượng chữ số của N.", "n = input().strip()\nprint(len(n))", "Đếm chữ số bằng len", "12345", "5"),
        ("C2_19", "Thông hiểu", "Kiểm tra tam giác hợp lệ", "Nhập 3 cạnh a, b, c trên 3 dòng. In `HOP LE` nếu lập thành tam giác, ngược lại `KHONG`.", "a,b,c = int(input()), int(input()), int(input())\nprint('HOP LE' if a+b>c and a+c>b and b+c>a else 'KHONG')", "Bất đẳng thức tam giác", "3\n4\n5", "HOP LE"),
        ("C2_20", "Thông hiểu", "Xếp loại học lực theo điểm", "Nhập điểm d. Nếu d >= 8 in `GIOI`, d >= 5 in `DAT`, còn lại `CHUA DAT`.", "d = float(input())\nprint('GIOI' if d>=8 else ('DAT' if d>=5 else 'CHUA DAT'))", "Rẽ nhánh lồng nhau", "8.5", "GIOI"),

        # --- 10 bài Vận dụng (C2_21 -> C2_30) ---
        ("C2_21", "Vận dụng", "Tìm số lớn nhất trong 3 số", "Nhập 3 số a, b, c trên 3 dòng. In số lớn nhất.", "a,b,c = int(input()), int(input()), int(input())\nprint(max(a, b, c))", "Max 3 số", "10\n45\n23", "45"),
        ("C2_22", "Vận dụng", "Kiểm tra số nguyên tố", "Nhập số nguyên n. In `YES` nếu là số nguyên tố, ngược lại `NO`.", "n = int(input())\ndef isp(x):\n if x < 2: return False\n for i in range(2, int(x**0.5)+1):\n  if x%i==0: return False\n return True\nprint('YES' if isp(n) else 'NO')", "Thuật toán kiểm tra số nguyên tố", "7", "YES"),
        ("C2_23", "Vận dụng", "Kiểm tra năm nhuận", "Nhập năm y. In `NHUAN` nếu là năm nhuận, ngược lại in `KHONG`.", "y = int(input())\nprint('NHUAN' if (y%400==0 or (y%4==0 and y%100!=0)) else 'KHONG')", "Quy luật năm nhuận", "2024", "NHUAN"),
        ("C2_24", "Vận dụng", "Giải phương trình ax + b = 0", "Nhập a khác 0 và b trên 2 dòng. In nghiệm x = -b/a.", "a, b = float(input()), float(input())\nprint(-b / a)", "Phương trình bậc nhất", "2\n-4", "2.0"),
        ("C2_25", "Vận dụng", "Tính tổng các chữ số của N", "Nhập số nguyên N. In tổng các chữ số cấu thành số đó.", "s = input().strip()\nprint(sum(int(c) for c in s))", "Tách và cộng chữ số", "123", "6"),
        ("C2_26", "Vận dụng", "Ước chung lớn nhất (UCLN)", "Nhập 2 số nguyên a và b trên 2 dòng. In UCLN của chúng.", "import math\nprint(math.gcd(int(input()), int(input())))", "Thuật toán Euclid tìm UCLN", "24\n36", "12"),
        ("C2_27", "Vận dụng", "Bội chung nhỏ nhất (BCNN)", "Nhập 2 số nguyên a và b trên 2 dòng. In BCNN của chúng.", "import math\nprint(math.lcm(int(input()), int(input())))", "Hàm math.lcm", "4\n6", "12"),
        ("C2_28", "Vận dụng", "In bảng cửu chương K", "Nhập số K. In 3 phép nhân đầu tiên k*1, k*2, k*3 cách nhau bởi dấu cách.", "k = int(input())\nprint(f'{k*1} {k*2} {k*3}')", "Bảng cửu chương", "5", "5 10 15"),
        ("C2_29", "Vận dụng", "Đếm số lượng ước chẵn", "Nhập N. Đếm số lượng ước nguyên dương chẵn của N.", "n = int(input())\nprint(sum(1 for i in range(1, n+1) if n % i == 0 and i % 2 == 0))", "Ước chẵn", "12", "4"),
        ("C2_30", "Vận dụng", "Tổng bình phương 1 đến N", "Nhập N. In tổng 1^2 + 2^2 + ... + N^2.", "n = int(input())\nprint(sum(i*i for i in range(1, n+1)))", "Tổng bình phương", "3", "14"),

        # --- 10 bài Vận dụng cao (C2_31 -> C2_40) ---
        ("C2_31", "Vận dụng cao", "Kiểm tra số hoàn hảo", "Số hoàn hảo bằng tổng các ước nhỏ hơn nó. Nhập N, in `YES` hoặc `NO`.", "n = int(input())\nprint('YES' if sum(i for i in range(1, n) if n % i == 0) == n else 'NO')", "Định nghĩa số hoàn hảo", "6", "YES"),
        ("C2_32", "Vận dụng cao", "In số Fibonacci thứ N", "Dãy Fib: 1, 1, 2, 3, 5, 8... Nhập N, in số Fibonacci thứ N.", "n = int(input())\na, b = 1, 1\nfor _ in range(n - 1): a, b = b, a + b\nprint(a)", "Dãy Fibonacci", "6", "8"),
        ("C2_33", "Vận dụng cao", "Kiểm tra số đối xứng (Palindrome)", "Nhập số nguyên N. In `YES` nếu đọc xuôi ngược như nhau, ngược lại `NO`.", "s = input().strip()\nprint('YES' if s == s[::-1] else 'NO')", "Kiểm tra Palindrome", "12321", "YES"),
        ("C2_34", "Vận dụng cao", "Đếm số nguyên tố trong đoạn [1, N]", "Nhập N. Đếm xem có bao nhiêu số nguyên tố <= N.", "n = int(input())\ndef isp(x):\n if x<2: return False\n for i in range(2, int(x**0.5)+1):\n  if x%i==0: return False\n return True\nprint(sum(1 for i in range(1, n+1) if isp(i)))", "Sàng nguyên tố", "10", "4"),
        ("C2_35", "Vận dụng cao", "Tính tiền điện bậc thang", "Dưới 50 số giá 1500đ/số, từ số 51 trở đi giá 2000đ/số. Nhập số điện x, in tổng tiền.", "x = int(input())\nprint(x * 1500 if x <= 50 else 50 * 1500 + (x - 50) * 2000)", "Bậc thang tính tiền điện", "60", "95000"),
        ("C2_36", "Vận dụng cao", "Tìm chữ số lớn nhất của N", "Nhập số nguyên N. In ra chữ số có giá trị lớn nhất trong N.", "s = input().strip()\nprint(max(s))", "Cực trị chữ số", "48291", "9"),
        ("C2_37", "Vận dụng cao", "Tìm ước nguyên tố nhỏ nhất khác 1", "Nhập hợp số N. Tìm ước nguyên tố nhỏ nhất của N.", "n = int(input())\nfor i in range(2, n+1):\n if n % i == 0: print(i); break", "Ước nguyên tố nhỏ nhất", "35", "5"),
        ("C2_38", "Vận dụng cao", "Tổng phân số 1 + 1/2 + ... + 1/N", "Nhập N. In tổng chuỗi làm tròn 2 chữ số thập phân.", "n = int(input())\nprint(round(sum(1/i for i in range(1, n+1)), 2))", "Chuỗi điều hòa", "2", "1.5"),
        ("C2_39", "Vận dụng cao", "Kiểm tra lũy thừa của 2", "Nhập n > 0. In `YES` nếu n có dạng 2^k, ngược lại in `NO`.", "n = int(input())\nprint('YES' if n > 0 and (n & (n - 1)) == 0 else 'NO')", "Kiểm tra lũy thừa nhị phân", "16", "YES"),
        ("C2_40", "Vận dụng cao", "Đếm số bước giảm Collatz", "Nếu n chẵn n = n//2, lẻ n = 3n+1. Đếm số bước để n về 1.", "n = int(input())\nc = 0\nwhile n > 1:\n n = n // 2 if n % 2 == 0 else 3*n + 1\n c += 1\nprint(c)", "Phỏng đoán Collatz", "6", "8")
    ]
    return [{"id": d[0], "chapter": "Chương 2: Rẽ nhánh & Vòng lặp (Bài 19-21)", "difficulty": d[1], "title": d[2], "desc": d[3], "hint": d[4], "concept": d[5], "tests": [{"input": d[6], "expected": d[7]}]} for d in data]

def get_c3_exercises():
    data = [
        # --- 10 bài Nhận biết (C3_01 -> C3_10) ---
        ("C3_01", "Nhận biết", "Độ dài xâu ký tự", "Nhập một xâu s từ bàn phím. In ra độ dài của xâu.", "s = input()\nprint(len(s))", "Hàm len() của xâu", "EduCoder", "8"),
        ("C3_02", "Nhận biết", "Ký tự đầu tiên của xâu", "Nhập xâu s. In ký tự đầu tiên s[0].", "s = input()\nprint(s[0])", "Chỉ số đầu tiên s[0]", "Python", "P"),
        ("C3_03", "Nhận biết", "Ký tự cuối cùng của xâu", "Nhập xâu s. In ký tự cuối cùng s[-1].", "s = input()\nprint(s[-1])", "Chỉ số âm s[-1]", "Python", "n"),
        ("C3_04", "Nhận biết", "Chuyển xâu thành chữ in hoa", "Nhập xâu s. In xâu dưới dạng chữ in hoa.", "s = input()\nprint(s.upper())", "Phương thức upper()", "python", "PYTHON"),
        ("C3_05", "Nhận biết", "Chuyển xâu thành chữ in thường", "Nhập xâu s. In xâu dưới dạng chữ in thường.", "s = input()\nprint(s.lower())", "Phương thức lower()", "PYTHON", "python"),
        ("C3_06", "Nhận biết", "Độ dài danh sách List", "Cho danh sách có 4 phần tử. Hãy in số lượng phần tử của danh sách đó.", "print(4)", "Độ dài danh sách", "", "4"),
        ("C3_07", "Nhận biết", "Phần tử đầu của danh sách", "Nhập dòng các số cách nhau dấu cách. In phần tử đầu tiên.", "lst = input().split()\nprint(lst[0])", "Truy cập mảng a[0]", "10 20 30", "10"),
        ("C3_08", "Nhận biết", "Phần tử cuối của danh sách", "Nhập dòng các số cách nhau dấu cách. In phần tử cuối cùng.", "lst = input().split()\nprint(lst[-1])", "Truy cập mảng a[-1]", "10 20 30", "30"),
        ("C3_09", "Nhận biết", "Cắt lát 3 ký tự đầu", "Nhập xâu s dài ít nhất 3 ký tự. In 3 ký tự đầu tiên.", "s = input()\nprint(s[:3])", "Cắt lát chuỗi s[:3]", "Informatics", "Inf"),
        ("C3_10", "Nhận biết", "Nối hai xâu ký tự", "Dòng 1 xâu a, dòng 2 xâu b. In ra xâu ghép nối a + b.", "a, b = input(), input()\nprint(a + b)", "Toán tử nối chuỗi +", "Hello\nWorld", "HelloWorld"),

        # --- 10 bài Thông hiểu (C3_11 -> C3_20) ---
        ("C3_11", "Thông hiểu", "Đếm số phần tử chẵn trong List", "Dòng 1 số N. Dòng 2 N số nguyên. Đếm số lượng số chẵn.", "n = int(input())\nlst = list(map(int, input().split()))\nprint(sum(1 for x in lst if x % 2 == 0))", "Duyệt List kiểm tra chẵn", "5\n1 2 4 7 8", "3"),
        ("C3_12", "Thông hiểu", "Tính tổng các phần tử trong List", "Dòng 1 số N. Dòng 2 N số nguyên. In tổng các phần tử.", "n = int(input())\nlst = list(map(int, input().split()))\nprint(sum(lst))", "Hàm sum() trên List", "4\n5 10 15 20", "50"),
        ("C3_13", "Thông hiểu", "Tìm số lớn nhất trong danh sách", "Dòng 1 số N. Dòng 2 N số. In phần tử lớn nhất.", "n = int(input())\nlst = list(map(int, input().split()))\nprint(max(lst))", "Hàm max() trên List", "4\n3 9 2 7", "9"),
        ("C3_14", "Thông hiểu", "Tìm số nhỏ nhất trong danh sách", "Dòng 1 số N. Dòng 2 N số. In phần tử nhỏ nhất.", "n = int(input())\nlst = list(map(int, input().split()))\nprint(min(lst))", "Hàm min() trên List", "4\n3 9 2 7", "2"),
        ("C3_15", "Thông hiểu", "Đếm số từ trong câu", "Nhập một câu văn. Đếm xem câu đó có bao nhiêu từ.", "s = input().split()\nprint(len(s))", "Phương thức split()", "Tin hoc lop 10", "4"),
        ("C3_16", "Thông hiểu", "Đếm số lần xuất hiện ký tự 'a'", "Nhập xâu s. Đếm số lần ký tự 'a' xuất hiện trong xâu.", "s = input()\nprint(s.count('a'))", "Phương thức count()", "banana", "3"),
        ("C3_17", "Thông hiểu", "Kiểm tra từ có trong xâu", "Dòng 1 xâu cha, dòng 2 từ con. In `CO` nếu từ con xuất hiện trong xâu, ngược lại `KHONG`.", "s, k = input(), input()\nprint('CO' if k in s else 'KHONG')", "Toán tử in kiểm tra chuỗi", "Lap trinh Python\nPython", "CO"),
        ("C3_18", "Thông hiểu", "Thay thế ký tự trong xâu", "Nhập xâu s. Thay thế toàn bộ dấu cách `' '` bằng gạch dưới `'_'`.", "s = input()\nprint(s.replace(' ', '_'))", "Phương thức replace()", "hoc python vui", "hoc_python_vui"),
        ("C3_19", "Thông hiểu", "Đếm số lượng số dương trong List", "Dòng 1 số N. Dòng 2 N số nguyên. Đếm số lượng số > 0.", "n = int(input())\nlst = list(map(int, input().split()))\nprint(sum(1 for x in lst if x > 0))", "Lọc điều kiện > 0", "5\n-2 3 0 5 -1", "2"),
        ("C3_20", "Thông hiểu", "Kiểm tra phần tử X có trong List", "Dòng 1 dãy số. Dòng 2 số X. In `YES` nếu X có trong danh sách, ngược lại `NO`.", "lst = list(map(int, input().split()))\nx = int(input())\nprint('YES' if x in lst else 'NO')", "Toán tử in trên danh sách", "1 3 5 7\n5", "YES"),

        # --- 10 bài Vận dụng (C3_21 -> C3_30) ---
        ("C3_21", "Vận dụng", "Đảo ngược xâu ký tự", "Nhập xâu s từ bàn phím. In ra xâu đảo ngược của s.", "s = input()\nprint(s[::-1])", "Cắt lát chuỗi bước âm [::-1]", "Python", "nohtyP"),
        ("C3_22", "Vận dụng", "Kiểm tra xâu đối xứng", "Nhập xâu s. In `YES` nếu s đối xứng, ngược lại in `NO`.", "s = input()\nprint('YES' if s == s[::-1] else 'NO')", "Kiểm tra Palindrome xâu", "radar", "YES"),
        ("C3_23", "Vận dụng", "Tính trung bình cộng các số dương", "Dòng 1 N. Dòng 2 N số nguyên. In trung bình cộng các số > 0 làm tròn 1 chữ số.", "n = int(input())\nlst = [x for x in map(int, input().split()) if x > 0]\nprint(round(sum(lst)/len(lst), 1))", "Lọc và tính TBC", "5\n2 -3 4 6 -1", "4.0"),
        ("C3_24", "Vận dụng", "Sắp xếp danh sách tăng dần", "Dòng 1 N. Dòng 2 N số. In danh sách sau khi sắp xếp tăng dần cách nhau dấu cách.", "n = int(input())\nlst = sorted(map(int, input().split()))\nprint(*lst)", "Hàm sorted()", "5\n8 3 1 9 4", "1 3 4 8 9"),
        ("C3_25", "Vận dụng", "Sắp xếp danh sách giảm dần", "Dòng 1 N. Dòng 2 N số. In danh sách giảm dần cách nhau dấu cách.", "n = int(input())\nlst = sorted(map(int, input().split()), reverse=True)\nprint(*lst)", "Sắp xếp ngược reverse=True", "4\n2 9 5 1", "9 5 2 1"),
        ("C3_26", "Vận dụng", "Đếm số chữ cái in hoa", "Nhập xâu s. Đếm số lượng chữ cái in hoa trong xâu.", "s = input()\nprint(sum(1 for c in s if c.isupper()))", "Phương thức isupper()", "EduCoder Ten", "3"),
        ("C3_27", "Vận dụng", "Lọc danh sách chỉ lấy số chẵn", "Dòng 1 N. Dòng 2 N số. In các phần tử chẵn cách nhau dấu cách.", "n = int(input())\nlst = [x for x in input().split() if int(x) % 2 == 0]\nprint(*lst)", "List comprehension lọc chẵn", "5\n1 2 3 4 6", "2 4 6"),
        ("C3_28", "Vận dụng", "Tìm chỉ số đầu tiên của phần tử X", "Dòng 1 dãy số. Dòng 2 số X. In vị trí đầu tiên của X (bắt đầu từ 0). Nếu không có in `-1`.", "lst = list(map(int, input().split()))\nx = int(input())\nprint(lst.index(x) if x in lst else -1)", "Phương thức index()", "10 20 30 20\n20", "1"),
        ("C3_29", "Vận dụng", "Nhân đôi từng phần tử trong List", "Dòng 1 N. Dòng 2 N số. In danh sách sau khi nhân đôi mỗi phần tử.", "n = int(input())\nprint(*(int(x)*2 for x in input().split()))", "Biến đổi phần tử List", "3\n1 2 3", "2 4 6"),
        ("C3_30", "Vận dụng", "Cắt bỏ khoảng trắng hai đầu", "Nhập xâu s có khoảng trắng thừa ở hai đầu. In ra xâu sau khi loại bỏ khoảng trắng thừa.", "s = input()\nprint(s.strip())", "Phương thức strip()", "   Xin chao   ", "Xin chao"),

        # --- 10 bài Vận dụng cao (C3_31 -> C3_40) ---
        ("C3_31", "Vận dụng cao", "Xóa phần tử trùng lặp trong List", "Dòng 1 N. Dòng 2 N số. In các số duy nhất theo đúng thứ tự xuất hiện đầu tiên.", "n = int(input())\nlst = input().split()\nres = []\nfor x in lst:\n if x not in res: res.append(x)\nprint(*res)", "Khử trùng lặp giữ nguyên thứ tự", "6\n1 2 2 3 1 4", "1 2 3 4"),
        ("C3_32", "Vận dụng cao", "Tìm phần tử lớn thứ nhì trong List", "Dòng 1 N số khác nhau. In phần tử lớn thứ hai.", "lst = sorted(set(map(int, input().split())))\nprint(lst[-2])", "Tìm max thứ nhì", "5\n10 40 20 50 30", "40"),
        ("C3_33", "Vận dụng cao", "Chuẩn hóa họ tên", "Nhập họ tên viết hoa thường lộn xộn. In họ tên chuẩn hóa (chữ cái đầu viết hoa, cách nhau 1 khoảng trắng).", "s = ' '.join(w.capitalize() for w in input().split())\nprint(s)", "Chuẩn hóa xâu capitalize", "   nguYen   van   aN  ", "Nguyen Van An"),
        ("C3_34", "Vận dụng cao", "Tách số âm và số dương", "Dòng 1 N số. In các số âm trên dòng 1, các số dương trên dòng 2.", "lst = list(map(int, input().split()))\nprint(*(x for x in lst if x < 0))\nprint(*(x for x in lst if x > 0))", "Phân loại mảng", "-3 5 -1 2 4", "-3 -1\n5 2 4"),
        ("C3_35", "Vận dụng cao", "Kiểm tra danh sách đã sắp xếp tăng", "Dòng 1 N số. In `YES` nếu mảng đã sắp xếp tăng dần, ngược lại `NO`.", "lst = list(map(int, input().split()))\nprint('YES' if lst == sorted(lst) else 'NO')", "Kiểm tra tính đơn điệu", "1 3 5 8", "YES"),
        ("C3_36", "Vận dụng cao", "Tìm từ dài nhất trong câu", "Nhập một câu văn. In ra từ có độ dài lớn nhất trong câu.", "words = input().split()\nprint(max(words, key=len))", "Hàm max kèm key=len", "Hoc lap trinh Python", "Python"),
        ("C3_37", "Vận dụng cao", "Tích vô hướng hai vector", "Dòng 1 vector A (3 số). Dòng 2 vector B (3 số). In tích vô hướng a1*b1 + a2*b2 + a3*b3.", "a = list(map(int, input().split()))\nb = list(map(int, input().split()))\nprint(sum(x*y for x,y in zip(a,b)))", "Tích vô hướng mảng", "1 2 3\n4 5 6", "32"),
        ("C3_38", "Vận dụng cao", "Đếm số ký tự chữ số trong xâu", "Nhập xâu s gồm chữ và số. Đếm có bao nhiêu ký tự chữ số 0-9.", "s = input()\nprint(sum(1 for c in s if c.isdigit()))", "Phương thức isdigit()", "Lop10A1Nam2026", "5"),
        ("C3_39", "Vận dụng cao", "Xoay vòng mảng sang phải 1 vị trí", "Dòng 1 N số. Đưa phần tử cuối cùng lên đầu danh sách.", "lst = input().split()\nprint(*( [lst[-1]] + lst[:-1] ))", "Kỹ thuật xoay mảng", "1 2 3 4", "4 1 2 3"),
        ("C3_40", "Vận dụng cao", "Đếm số từ bắt đầu bằng chữ T", "Nhập một câu văn. Đếm số lượng từ bắt đầu bằng chữ 'T' hoặc 't'.", "s = input().split()\nprint(sum(1 for w in s if w.lower().startswith('t')))", "Phương thức startswith()", "Toi thich hoc Tin hoc", "3")
    ]
    return [{"id": d[0], "chapter": "Chương 3: Xâu ký tự & Kiểu List (Bài 22-25)", "difficulty": d[1], "title": d[2], "desc": d[3], "hint": d[4], "concept": d[5], "tests": [{"input": d[6], "expected": d[7]}]} for d in data]

def get_c4_exercises():
    data = [
        # --- 10 bài Nhận biết (C4_01 -> C4_10) ---
        ("C4_01", "Nhận biết", "Định nghĩa hàm tính bình phương", "Nhập số nguyên n. Viết hàm `binh_phuong(x)` trả về x^2 và in ra.", "def binh_phuong(x): return x * x\nprint(binh_phuong(int(input())))", "Từ khóa def và return", "5", "25"),
        ("C4_02", "Nhận biết", "Hàm tính lập phương", "Nhập số n. Viết hàm `lap_phuong(x)` trả về x^3 và in ra.", "def lap_phuong(x): return x**3\nprint(lap_phuong(int(input())))", "Hàm 1 tham số", "3", "27"),
        ("C4_03", "Nhận biết", "Hàm trả về số đối", "Nhập số n. Viết hàm `so_doi(x)` trả về -x.", "def so_doi(x): return -x\nprint(so_doi(int(input())))", "Giá trị trả về", "10", "-10"),
        ("C4_04", "Nhận biết", "Hàm in lời chào theo tên", "Nhập tên s. Viết hàm `chao(name)` in ra: `Xin chao {name}!`.", "def chao(n): print(f'Xin chao {n}!')\nchao(input())", "Thủ tục không có return", "Nam", "Xin chao Nam!"),
        ("C4_05", "Nhận biết", "Hàm kiểm tra số âm", "Nhập số n. Viết hàm `is_negative(x)` trả về `True` nếu x < 0, ngược lại `False`.", "def is_negative(x): return x < 0\nprint(is_negative(int(input())))", "Hàm trả về kiểu bool", "-5", "True"),
        ("C4_06", "Nhận biết", "Hàm tính diện tích hình vuông", "Nhập cạnh a. Viết hàm `dt_vuong(a)` trả về a*a.", "def dt_vuong(a): return a*a\nprint(dt_vuong(int(input())))", "Hàm diện tích hình học", "4", "16"),
        ("C4_07", "Nhận biết", "Hàm tính chu vi hình vuông", "Nhập cạnh a. Viết hàm `cv_vuong(a)` trả về a*4.", "def cv_vuong(a): return a*4\nprint(cv_vuong(int(input())))", "Hàm chu vi hình học", "4", "16"),
        ("C4_08", "Nhận biết", "Hàm nhân đôi một số", "Nhập số n. Viết hàm `nhan_doi(x)` trả về x*2.", "def nhan_doi(x): return x*2\nprint(nhan_doi(int(input())))", "Tham số hình thức", "7", "14"),
        ("C4_09", "Nhận biết", "Hàm chia đôi một số", "Nhập số n. Viết hàm `chia_doi(x)` trả về x/2.", "def chia_doi(x): return x/2\nprint(chia_doi(int(input())))", "Phép toán trong hàm", "10", "5.0"),
        ("C4_10", "Nhận biết", "Hàm lấy giá trị tuyệt đối", "Nhập số n. Viết hàm `tuyet_doi(x)` trả về abs(x).", "def tuyet_doi(x): return abs(x)\nprint(tuyet_doi(int(input())))", "Hàm gọi hàm có sẵn", "-9", "9"),

        # --- 10 bài Thông hiểu (C4_11 -> C4_20) ---
        ("C4_11", "Thông hiểu", "Hàm tính lũy thừa cơ số", "Nhập cơ số a và số mũ b trên 2 dòng. Viết hàm `luy_thua(a, b)` trả về a^b.", "def luy_thua(a, b): return a ** b\nprint(luy_thua(int(input()), int(input())))", "Hàm nhiều tham số", "2\n3", "8"),
        ("C4_12", "Thông hiểu", "Hàm tính tổng hai số", "Nhập 2 số a và b trên 2 dòng. Viết hàm `tong(a, b)` trả về a + b.", "def tong(a, b): return a + b\nprint(tong(int(input()), int(input())))", "Tính toán trong hàm", "15\n25", "40"),
        ("C4_13", "Thông hiểu", "Hàm tìm số lớn nhất giữa 2 số", "Nhập 2 số a và b trên 2 dòng. Viết hàm `max_2(a, b)` trả về số lớn hơn.", "def max_2(a, b): return max(a, b)\nprint(max_2(int(input()), int(input())))", "Cực trị trong hàm", "10\n20", "20"),
        ("C4_14", "Thông hiểu", "Hàm kiểm tra số chẵn", "Nhập số n. Viết hàm `is_even(n)` trả về `True` nếu n chẵn, ngược lại `False`.", "def is_even(n): return n % 2 == 0\nprint(is_even(int(input())))", "Hàm logic kiểm tra chẵn", "6", "True"),
        ("C4_15", "Thông hiểu", "Hàm chu vi hình chữ nhật", "Nhập dài a và rộng b. Viết hàm `cv_hcn(a, b)` trả về (a+b)*2.", "def cv_hcn(a, b): return (a + b) * 2\nprint(cv_hcn(int(input()), int(input())))", "Chu vi HCN trong hàm", "4\n6", "20"),
        ("C4_16", "Thông hiểu", "Hàm tính diện tích tam giác", "Nhập đáy a và chiều cao h. Viết hàm `dt_tam_giac(a, h)` trả về a*h/2.", "def dt_tam_giac(a, h): return a * h / 2\nprint(dt_tam_giac(float(input()), float(input())))", "Diện tích tam giác", "4\n5", "10.0"),
        ("C4_17", "Thông hiểu", "Hàm kiểm tra chia hết", "Nhập a và b trên 2 dòng. Viết hàm `chia_het(a, b)` trả về `True` nếu a chia hết cho b.", "def chia_het(a, b): return a % b == 0\nprint(chia_het(int(input()), int(input())))", "Chia hết trong hàm", "10\n5", "True"),
        ("C4_18", "Thông hiểu", "Hàm tính tiền cước điện thoại", "Số phút p. Giá 1000đ/phút. Viết hàm `cuoc(p)` trả về tổng tiền.", "def cuoc(p): return p * 1000\nprint(cuoc(int(input())))", "Toán thực tế trong hàm", "12", "12000"),
        ("C4_19", "Thông hiểu", "Hàm nối chuỗi có khoảng trắng", "Dòng 1 xâu a, dòng 2 xâu b. Viết hàm `ghep(a, b)` trả về a + ' ' + b.", "def ghep(a, b): return a + ' ' + b\nprint(ghep(input(), input()))", "Xử lý chuỗi trong hàm", "Tin\nHoc", "Tin Hoc"),
        ("C4_20", "Thông hiểu", "Hàm làm tròn điểm thi", "Nhập điểm d. Viết hàm `lam_tron(d)` làm tròn 1 chữ số thập phân.", "def lam_tron(d): return round(d, 1)\nprint(lam_tron(float(input())))", "Làm tròn trong hàm", "7.666", "7.7"),

        # --- 10 bài Vận dụng (C4_21 -> C4_30) ---
        ("C4_21", "Vận dụng", "Hàm kiểm tra số nguyên tố", "Viết hàm `is_prime(n)`. Nhập n, in `YES` nếu là số nguyên tố, ngược lại `NO`.", "def is_prime(n):\n if n < 2: return False\n for i in range(2, int(n**0.5)+1):\n  if n % i == 0: return False\n return True\nprint('YES' if is_prime(int(input())) else 'NO')", "Xây dựng hàm kiểm tra nguyên tố", "11", "YES"),
        ("C4_22", "Vận dụng", "Hàm tính giai thừa N!", "Viết hàm `giai_thua(n)` trả về n!.", "import math\ndef giai_thua(n): return math.factorial(n)\nprint(giai_thua(int(input())))", "Tính toán giai thừa hàm", "5", "120"),
        ("C4_23", "Vận dụng", "Hàm tính tổng danh sách List", "Viết hàm `tong_mang(lst)` nhận danh sách số và trả về tổng các phần tử.", "def tong_mang(lst): return sum(lst)\nprint(tong_mang(list(map(int, input().split()))))", "Truyền List vào hàm", "1 2 3 4 5", "15"),
        ("C4_24", "Vận dụng", "Hàm tìm giá trị lớn nhất trong List", "Viết hàm `max_mang(lst)` trả về số lớn nhất trong mảng.", "def max_mang(lst): return max(lst)\nprint(max_mang(list(map(int, input().split()))))", "Tìm max trên mảng bằng hàm", "8 3 12 5", "12"),
        ("C4_25", "Vận dụng", "Hàm đếm số nguyên âm trong xâu", "Nhập xâu s. Viết hàm `dem_nguyen_am(s)` đếm chữ a, e, i, o, u.", "def dem_nguyen_am(s): return sum(1 for c in s.lower() if c in 'aeiou')\nprint(dem_nguyen_am(input()))", "Duyệt xâu trong hàm", "Vietnam", "3"),
        ("C4_26", "Vận dụng", "Hàm kiểm tra năm nhuận", "Viết hàm `nam_nhuan(y)` trả về `True` nếu y là năm nhuận.", "def nam_nhuan(y): return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)\nprint(nam_nhuan(int(input())))", "Hàm kiểm tra năm nhuận", "2000", "True"),
        ("C4_27", "Vận dụng", "Hàm tính chỉ số BMI", "Viết hàm `tinh_bmi(w, h)` nhận cân nặng và chiều cao, trả về BMI làm tròn 1 chữ số.", "def tinh_bmi(w, h): return round(w / (h * h), 1)\nprint(tinh_bmi(float(input()), float(input())))", "Hàm tính BMI", "60\n1.7", "20.8"),
        ("C4_28", "Vận dụng", "Hàm đếm số từ trong câu", "Viết hàm `so_tu(s)` nhận câu văn và trả về số lượng từ.", "def so_tu(s): return len(s.split())\nprint(so_tu(input()))", "Hàm đếm từ", "Chuc mung nam moi", "4"),
        ("C4_29", "Vận dụng", "Hàm đảo ngược chuỗi", "Viết hàm `dao_chuoi(s)` trả về chuỗi đảo ngược.", "def dao_chuoi(s): return s[::-1]\nprint(dao_chuoi(input()))", "Hàm đảo chuỗi", "HaNoi", "ioNaH"),
        ("C4_30", "Vận dụng", "Hàm tính trung bình cộng List", "Viết hàm `tbc(lst)` trả về trung bình cộng các số trong danh sách.", "def tbc(lst): return sum(lst) / len(lst)\nprint(tbc(list(map(int, input().split()))))", "Hàm tính TBC", "2 4 6 8", "5.0"),

        # --- 10 bài Vận dụng cao (C4_31 -> C4_40) ---
        ("C4_31", "Vận dụng cao", "Hàm tìm UCLN Euclid", "Nhập 2 số a và b. Viết hàm `ucln(a, b)` dùng thuật toán Euclid.", "import math\nprint(math.gcd(int(input()), int(input())))", "Thuật toán Euclid trong hàm", "24\n36", "12"),
        ("C4_32", "Vận dụng cao", "Hàm tính số Fibonacci thứ N", "Viết hàm `fib(n)` trả về số Fibonacci thứ n.", "def fib(n):\n a, b = 1, 1\n for _ in range(n - 1): a, b = b, a + b\n return a\nprint(fib(int(input())))", "Hàm tạo số Fibonacci", "7", "13"),
        ("C4_33", "Vận dụng cao", "Hàm kiểm tra số hoàn hảo", "Viết hàm `is_perfect(n)` trả về `True` nếu n là số hoàn hảo.", "def is_perfect(n): return sum(i for i in range(1, n) if n % i == 0) == n\nprint(is_perfect(int(input())))", "Hàm kiểm tra số hoàn hảo", "28", "True"),
        ("C4_34", "Vận dụng cao", "Hàm chuẩn hóa họ tên", "Viết hàm `chuan_hoa(name)` xóa khoảng trắng thừa và viết hoa chữ cái đầu mỗi từ.", "def chuan_hoa(s): return ' '.join(w.capitalize() for w in s.split())\nprint(chuan_hoa(input()))", "Hàm chuẩn hóa chuỗi", "  le   thi   hoa ", "Le Thi Hoa"),
        ("C4_35", "Vận dụng cao", "Hàm lọc các số nguyên tố trong List", "Viết hàm nhận danh sách và in các số nguyên tố có trong danh sách.", "def is_p(x):\n if x < 2: return False\n for i in range(2, int(x**0.5)+1):\n  if x%i==0: return False\n return True\nlst = list(map(int, input().split()))\nprint(*(x for x in lst if is_p(x)))", "Lọc nguyên tố mảng", "4 5 6 7 8 9 11", "5 7 11"),
        ("C4_36", "Vận dụng cao", "Hàm đệ quy tính tổng 1 đến N", "Viết hàm đệ quy `tong_de_quy(n)` tính tổng 1 + 2 + ... + N.", "def tong_dq(n):\n return 1 if n == 1 else n + tong_dq(n - 1)\nprint(tong_dq(int(input())))", "Đệ quy cơ bản", "5", "15"),
        ("C4_37", "Vận dụng cao", "Hàm đệ quy tính giai thừa", "Viết hàm đệ quy `gt_de_quy(n)` tính n!.", "def gt_dq(n):\n return 1 if n <= 1 else n * gt_dq(n - 1)\nprint(gt_dq(int(input())))", "Đệ quy giai thừa", "4", "24"),
        ("C4_38", "Vận dụng cao", "Hàm đếm số lượng số nguyên tố", "Nhập danh sách số. Viết hàm đếm có bao nhiêu số nguyên tố.", "def is_p(x):\n if x < 2: return False\n for i in range(2, int(x**0.5)+1):\n  if x%i==0: return False\n return True\nprint(sum(1 for x in map(int, input().split()) if is_p(x)))", "Đếm số nguyên tố trong hàm", "2 3 4 5 6", "3"),
        ("C4_39", "Vận dụng cao", "Hàm giải phương trình bậc nhất", "Viết hàm `pt_bac_1(a, b)` giải ax + b = 0. Trả về nghiệm x.", "def pt_bac_1(a, b): return -b / a\nprint(pt_bac_1(float(input()), float(input())))", "Phương trình trong hàm", "4\n-12", "3.0"),
        ("C4_40", "Vận dụng cao", "Hàm tính tổ hợp C(n, k)", "Nhập n và k trên 2 dòng (k <= n). Viết hàm tính C(n, k) = n! / (k! * (n-k)!).", "import math\nprint(math.comb(int(input()), int(input())))", "Hàm math.comb tổ hợp", "5\n2", "10")
    ]
    return [{"id": d[0], "chapter": "Chương 4: Hàm & Chương trình con (Bài 26-28)", "difficulty": d[1], "title": d[2], "desc": d[3], "hint": d[4], "concept": d[5], "tests": [{"input": d[6], "expected": d[7]}]} for d in data]

def get_c5_exercises():
    data = [
        # --- 10 bài Nhận biết (C5_01 -> C5_10) ---
        ("C5_01", "Nhận biết", "Bắt lỗi chia cho 0 đơn giản", "Thực hiện phép chia 10 cho 0 trong khối try-except. Bắt lỗi `ZeroDivisionError` và in `LOI CHIA CHO 0`.", "try:\n print(10 // 0)\nexcept ZeroDivisionError:\n print('LOI CHIA CHO 0')", "Bắt lỗi ZeroDivisionError", "", "LOI CHIA CHO 0"),
        ("C5_02", "Nhận biết", "Bắt lỗi ép kiểu ValueError", "Thử ép chuỗi `'abc'` sang số nguyên. Bắt `ValueError` và in `LOI EP KIEU`.", "try:\n int('abc')\nexcept ValueError:\n print('LOI EP KIEU')", "Bắt lỗi ValueError", "", "LOI EP KIEU"),
        ("C5_03", "Nhận biết", "Bắt lỗi vượt chỉ số IndexError", "Cho mảng `a = [1, 2]`. Thử in `a[5]` trong try-except và in `LOI CHI SO`.", "try:\n a = [1, 2]\n print(a[5])\nexcept IndexError:\n print('LOI CHI SO')", "Bắt lỗi IndexError", "", "LOI CHI SO"),
        ("C5_04", "Nhận biết", "Thuật toán đếm phần tử thỏa điều kiện", "Dòng 1 N. Dòng 2 N số. Đếm số lượng số > 10.", "n = int(input())\nprint(sum(1 for x in map(int, input().split()) if x > 10))", "Thuật toán đếm cơ bản", "4\n5 12 8 15", "2"),
        ("C5_05", "Nhận biết", "Thuật toán tính tổng tích lũy", "Dòng 1 N. Dòng 2 N số. In tổng tất cả các số trong mảng.", "n = int(input())\nprint(sum(map(int, input().split())))", "Thuật toán cộng dồn", "3\n10 20 30", "60"),
        ("C5_06", "Nhận biết", "Kiểm thử trường hợp biên số 0", "Nhập số n. In `ZERO` nếu n == 0, ngược lại in `NON-ZERO`.", "n = int(input())\nprint('ZERO' if n == 0 else 'NON-ZERO')", "Kiểm thử trường hợp biên", "0", "ZERO"),
        ("C5_07", "Nhận biết", "Tìm kiếm tuần tự cơ bản", "Dòng 1 N số. Dòng 2 khóa K. In `FOUND` nếu thấy K trong mảng.", "lst = input().split()\nk = input()\nprint('FOUND' if k in lst else 'NOT FOUND')", "Tìm kiếm tuyến tính cơ bản", "1 4 9 16\n9", "FOUND"),
        ("C5_08", "Nhận biết", "Thuật toán so sánh tìm số lớn nhất", "Nhập 2 số a và b. Dùng câu lệnh if để in số lớn hơn.", "a, b = int(input()), int(input())\nprint(a if a > b else b)", "So sánh cực trị cơ bản", "15\n8", "15"),
        ("C5_09", "Nhận biết", "Sắp xếp 3 số tăng dần", "Nhập 3 số nguyên cách nhau dấu cách. In ra 3 số tăng dần.", "lst = sorted(map(int, input().split()))\nprint(*lst)", "Thuật toán sắp xếp cơ bản", "5 1 4", "1 4 5"),
        ("C5_10", "Nhận biết", "Bắt lỗi tổng quát Exception", "Dùng khối `except Exception:` để bắt mọi lỗi và in `CO LOI XAY RA`.", "try:\n 1 / 0\nexcept Exception:\n print('CO LOI XAY RA')", "Khối Exception tổng quát", "", "CO LOI XAY RA"),

        # --- 10 bài Thông hiểu (C5_11 -> C5_20) ---
        ("C5_11", "Thông hiểu", "Tìm số lớn nhất trong dãy", "Dòng 1 N số nguyên. In phần tử lớn nhất.", "lst = list(map(int, input().split()))\nprint(max(lst))", "Thuật toán tìm cực trị Max", "5\n3 9 1 12 7", "12"),
        ("C5_12", "Thông hiểu", "Tìm vị trí đầu tiên của khóa K (Linear Search)", "Dòng 1 N số. Dòng 2 khóa K. In vị trí đầu tiên xuất hiện K (bắt đầu từ 0). Nếu không thấy in `-1`.", "lst = list(map(int, input().split()))\nk = int(input())\nprint(lst.index(k) if k in lst else -1)", "Thuật toán tìm kiếm tuần tự", "10 25 30 25 40\n25", "1"),
        ("C5_13", "Thông hiểu", "Bắt lỗi chia hai số nhập vào", "Nhập 2 số a và b trên 2 dòng. In kết quả `a // b`. Nếu b = 0 in `KHONG THE CHIA CHO 0`.", "a, b = int(input()), int(input())\ntry:\n print(a // b)\nexcept ZeroDivisionError:\n print('KHONG THE CHIA CHO 0')", "Xử lý ZeroDivisionError", "10\n0", "KHONG THE CHIA CHO 0"),
        ("C5_14", "Thông hiểu", "Xử lý nhập số nguyên hợp lệ", "Nhập một chuỗi. Thử ép sang số nguyên và in `DUNG SO NGUYEN`. Nếu lỗi ValueError in `SAI DINH DANG`.", "try:\n int(input())\n print('DUNG SO NGUYEN')\nexcept ValueError:\n print('SAI DINH DANG')", "Bắt lỗi ép kiểu ValueError", "123a", "SAI DINH DANG"),
        ("C5_15", "Thông hiểu", "Đếm số lần xuất hiện của phần tử X", "Dòng 1 N số. Dòng 2 số X. Đếm X xuất hiện bao nhiêu lần trong danh sách.", "lst = list(map(int, input().split()))\nx = int(input())\nprint(lst.count(x))", "Thuật toán đếm tần suất", "1 2 2 3 2 4\n2", "3"),
        ("C5_16", "Thông hiểu", "Tìm giá trị nhỏ nhất và vị trí của nó", "Dòng 1 N số. In giá trị nhỏ nhất và chỉ số đầu tiên của nó cách nhau dấu cách.", "lst = list(map(int, input().split()))\nm = min(lst)\nprint(m, lst.index(m))", "Tìm Min kèm chỉ số", "7 2 9 2 5", "2 1"),
        ("C5_17", "Thông hiểu", "Kiểm tra mảng đối xứng", "Dòng 1 N số. In `YES` nếu mảng đối xứng, ngược lại `NO`.", "lst = input().split()\nprint('YES' if lst == lst[::-1] else 'NO')", "Kiểm tra mảng đối xứng", "1 2 3 2 1", "YES"),
        ("C5_18", "Thông hiểu", "Tìm kiếm trong mảng đã sắp xếp", "Cho dãy đã sắp xếp tăng. Tìm khóa K, in `CO` hoặc `KHONG`.", "lst = list(map(int, input().split()))\nk = int(input())\nprint('CO' if k in lst else 'KHONG')", "Tìm kiếm trên mảng đã sắp xếp", "2 4 6 8 10\n8", "CO"),
        ("C5_19", "Thông hiểu", "Sắp xếp dãy số tăng dần", "Dòng 1 N số. In dãy số sau khi sắp xếp tăng dần.", "lst = sorted(map(int, input().split()))\nprint(*lst)", "Thuật toán sắp xếp tăng", "5 2 9 1", "1 2 5 9"),
        ("C5_20", "Thông hiểu", "Kiểm thử trường hợp mảng rỗng", "Nhập một chuỗi các số (có thể rỗng). Nếu rỗng in `RONG`, ngược lại in số lượng phần tử.", "s = input().strip()\nprint('RONG' if not s else len(s.split()))", "Kiểm thử biên rỗng", "", "RONG"),

        # --- 10 bài Vận dụng (C5_21 -> C5_30) ---
        ("C5_21", "Vận dụng", "Sắp xếp nổi bọt (Bubble Sort)", "Dòng 1 N số. Thực hiện thuật toán sắp xếp nổi bọt và in mảng tăng dần.", "lst = list(map(int, input().split()))\nfor i in range(len(lst)):\n for j in range(len(lst)-1-i):\n  if lst[j] > lst[j+1]: lst[j], lst[j+1] = lst[j+1], lst[j]\nprint(*lst)", "Thuật toán Bubble Sort", "4 3 2 1", "1 2 3 4"),
        ("C5_22", "Vận dụng", "Tìm tất cả vị trí xuất hiện của X", "Dòng 1 N số. Dòng 2 khóa X. In tất cả các chỉ số (từ 0) xuất hiện X cách nhau dấu cách. Nếu không có in `-1`.", "lst = list(map(int, input().split()))\nx = int(input())\npos = [str(i) for i, v in enumerate(lst) if v == x]\nprint(' '.join(pos) if pos else -1)", "Tìm kiếm đa vị trí", "5 2 5 5 1\n5", "0 2 3"),
        ("C5_23", "Vận dụng", "Tìm số dương nhỏ nhất trong mảng", "Dòng 1 N số gồm cả âm và dương. In số dương nhỏ nhất trong mảng.", "lst = [x for x in map(int, input().split()) if x > 0]\nprint(min(lst) if lst else -1)", "Lọc và tìm Min dương", "-5 8 -2 3 10", "3"),
        ("C5_24", "Vận dụng", "Kiểm tra mảng tăng ngặt", "Dòng 1 N số. In `YES` nếu mỗi phần tử đều strictly lớn hơn phần tử đứng trước, ngược lại `NO`.", "lst = list(map(int, input().split()))\nprint('YES' if all(lst[i] < lst[i+1] for i in range(len(lst)-1)) else 'NO')", "Kiểm tra tính tăng ngặt", "1 3 7 9", "YES"),
        ("C5_25", "Vận dụng", "Sắp xếp chọn (Selection Sort)", "Dòng 1 N số. Sắp xếp tăng dần bằng Selection Sort và in kết quả.", "lst = sorted(map(int, input().split()))\nprint(*lst)", "Thuật toán Selection Sort", "9 2 6 4", "2 4 6 9"),
        ("C5_26", "Vận dụng", "Khoảng cách nhỏ nhất giữa 2 phần tử liền kề", "Dòng 1 N số đã sắp xếp tăng. Tìm khoảng cách nhỏ nhất giữa 2 phần tử liền kề.", "lst = sorted(map(int, input().split()))\nprint(min(lst[i+1]-lst[i] for i in range(len(lst)-1)))", "Khoảng cách nhỏ nhất mảng", "1 5 8 10", "2"),
        ("C5_27", "Vận dụng", "Bắt lỗi nhập mảng chỉ toàn số", "Nhập chuỗi các từ. Nếu tất cả đều là số nguyên in `HOP LE`, nếu có từ chứa chữ cái in `CHUA KY TU`.", "s = input().split()\ntry:\n [int(x) for x in s]\n print('HOP LE')\nexcept ValueError:\n print('CHUA KY TU')", "Kiểm tra kiểu dữ liệu toàn mảng", "10 20 abc 40", "CHUA KY TU"),
        ("C5_28", "Vận dụng", "Đếm số cặp số bằng nhau", "Dòng 1 N số. Đếm có bao nhiêu cặp chỉ số (i < j) mà lst[i] == lst[j].", "lst = list(map(int, input().split()))\nprint(sum(1 for i in range(len(lst)) for j in range(i+1, len(lst)) if lst[i]==lst[j]))", "Thuật toán đếm cặp bằng nhau", "1 2 1 2 1", "4"),
        ("C5_29", "Vận dụng", "Tìm phần tử xuất hiện đúng 1 lần", "Dòng 1 N số. In phần tử đầu tiên chỉ xuất hiện duy nhất 1 lần trong mảng.", "lst = list(map(int, input().split()))\nfor x in lst:\n if lst.count(x) == 1: print(x); break", "Tìm phần tử duy nhất", "2 3 2 4 3", "4"),
        ("C5_30", "Vận dụng", "Tìm số bị thiếu trong dãy 1 đến N", "Dòng 1 dãy số từ 1 đến N nhưng bị thiếu mất 1 số. Dòng 2 giá trị N. Tìm số bị thiếu.", "lst = list(map(int, input().split()))\nn = int(input())\nprint(n*(n+1)//2 - sum(lst))", "Thuật toán tổng sai phân", "1 2 4 5\n5", "3"),

        # --- 10 bài Vận dụng cao (C5_31 -> C5_40) ---
        ("C5_31", "Vận dụng cao", "Trộn hai mảng đã sắp xếp (Merge Step)", "Dòng 1 mảng A tăng dần. Dòng 2 mảng B tăng dần. In mảng hợp nhất đã sắp xếp tăng dần.", "a = list(map(int, input().split()))\nb = list(map(int, input().split()))\nprint(*sorted(a + b))", "Kỹ thuật trộn mảng Merge Sort", "1 3 5\n2 4 6", "1 2 3 4 5 6"),
        ("C5_32", "Vận dụng cao", "Tìm phần tử đa số (Majority Element)", "Dòng 1 N số. Phần tử đa số xuất hiện nhiều hơn N/2 lần. In phần tử đó hoặc `-1`.", "lst = list(map(int, input().split()))\nfrom collections import Counter\nc = Counter(lst).most_common(1)[0]\nprint(c[0] if c[1] > len(lst)//2 else -1)", "Thuật toán Majority Element", "2 2 1 2 3 2 2", "2"),
        ("C5_33", "Vận dụng cao", "Tìm tổng đoạn con lớn nhất (Kadane)", "Dòng 1 N số nguyên. Tìm tổng đoạn con liên tiếp lớn nhất.", "lst = list(map(int, input().split()))\nmax_s = cur = lst[0]\nfor x in lst[1:]:\n cur = max(x, cur + x)\n max_s = max(max_s, cur)\nprint(max_s)", "Thuật toán Kadane", "-2 1 -3 4 -1 2 1 -5 4", "6"),
        ("C5_34", "Vận dụng cao", "Kiểm tra dãy ngoặc đơn hợp lệ", "Nhập chuỗi chỉ gồm ký tự `(` và `)`. In `YES` nếu đóng mở hợp lệ, ngược lại `NO`.", "s = input().strip()\nbal = 0\nok = True\nfor c in s:\n if c == '(': bal += 1\n elif c == ')': bal -= 1\n if bal < 0: ok = False; break\nprint('YES' if ok and bal == 0 else 'NO')", "Thuật toán kiểm tra dãy ngoặc", "(())()", "YES"),
        ("C5_35", "Vận dụng cao", "Tìm cặp số có tổng bằng K (Two Sum)", "Dòng 1 N số. Dòng 2 tổng K. In `YES` nếu tồn tại 2 phần tử có tổng bằng K, ngược lại `NO`.", "lst = list(map(int, input().split()))\nk = int(input())\ns = set()\nok = False\nfor x in lst:\n if k - x in s: ok = True; break\n s.add(x)\nprint('YES' if ok else 'NO')", "Bài toán Two Sum cơ bản", "2 7 11 15\n9", "YES"),
        ("C5_36", "Vận dụng cao", "Bắt lỗi ngoại lệ đa tầng", "Nhập a và b trên 2 dòng. Nếu b = 0 in `LOI CHIA 0`, nếu a hoặc b không phải số in `LOI DINH DANG`, ngược lại in a // b.", "try:\n a, b = int(input()), int(input())\n print(a // b)\nexcept ValueError:\n print('LOI DINH DANG')\nexcept ZeroDivisionError:\n print('LOI CHIA 0')", "Bắt nhiều ngoại lệ đa tầng", "10\n0", "LOI CHIA 0"),
        ("C5_37", "Vận dụng cao", "Tìm số nguyên tố lớn nhất nhỏ hơn N", "Nhập N > 2. Tìm số nguyên tố lớn nhất < N.", "n = int(input())\ndef is_p(x):\n for i in range(2, int(x**0.5)+1):\n  if x%i==0: return False\n return True\nfor x in range(n-1, 1, -1):\n if is_p(x): print(x); break", "Tìm số nguyên tố cận trên", "20", "19"),
        ("C5_38", "Vận dụng cao", "Độ dài dãy con tăng liên tiếp dài nhất", "Dòng 1 N số. In độ dài dãy tăng liên tiếp dài nhất trong mảng.", "lst = list(map(int, input().split()))\nmax_l = cur = 1\nfor i in range(len(lst)-1):\n if lst[i] < lst[i+1]: cur += 1; max_l = max(max_l, cur)\n else: cur = 1\nprint(max_l)", "Dãy con tăng liên tiếp", "1 2 2 3 4 1", "3"),
        ("C5_39", "Vận dụng cao", "Mã hóa dịch chuyển Caesar", "Nhập xâu chữ thường và bước dịch k trên 2 dòng. In xâu sau khi dịch vòng trong bảng chữ cái tiếng Anh.", "s = input().strip()\nk = int(input())\nprint(''.join(chr((ord(c)-97+k)%26 + 97) for c in s))", "Mã hóa Caesar Cipher", "abc\n3", "def"),
        ("C5_40", "Vận dụng cao", "Tìm vị trí số âm đầu tiên", "Dòng 1 N số. In chỉ số (từ 0) của số âm đầu tiên. Nếu toàn số dương in `-1`.", "lst = list(map(int, input().split()))\nres = -1\nfor i, x in enumerate(lst):\n if x < 0: res = i; break\nprint(res)", "Tìm kiếm biên âm trên mảng", "4 8 -3 2 -5", "2")
    ]
    return [{"id": d[0], "chapter": "Chương 5: Thuật toán & Gỡ lỗi (Bài 29-30)", "difficulty": d[1], "title": d[2], "desc": d[3], "hint": d[4], "concept": d[5], "tests": [{"input": d[6], "expected": d[7]}]} for d in data]

def build_all_exercises():
    return get_c1_exercises() + get_c2_exercises() + get_c3_exercises() + get_c4_exercises() + get_c5_exercises()

REAL_EXERCISES = build_all_exercises()
def map_exercise_to_concept(ex_id: str, title: str, desc: str) -> str:
    text_corpus = f"{ex_id} {title} {desc}".lower()
    
    if "bubble sort" in text_corpus or "sắp xếp" in text_corpus or "selection sort" in text_corpus:
        return "thuat_toan_sap_xep"
    elif "tìm kiếm" in text_corpus or "vị trí xuất hiện" in text_corpus or "two sum" in text_corpus:
        return "thuat_toan_tim_kiem"
    elif "xâu" in text_corpus or "chuỗi" in text_corpus or "ký tự" in text_corpus or "ngoặc" in text_corpus:
        return "kieu_du_lieu_xau"
    elif "mảng" in text_corpus or "danh sách" in text_corpus or "lst" in text_corpus or ex_id.startswith("C5"):
        return "kieu_du_lieu_danh_sach"
    elif "while" in text_corpus:
        return "vong_lap_while"
    elif "for" in text_corpus or "dãy số" in text_corpus:
        return "vong_lap_for"
    elif "if" in text_corpus or "chẵn" in text_corpus or "lẻ" in text_corpus:
        return "cau_lenh_if"
    else:
        return "bien_va_kieu_du_lieu"

def get_all_exercises_standardized() -> list:
    standardized_list = []
    
    for item in REAL_EXERCISES:
        if isinstance(item, tuple):
            ex_id = item[0]
            level = item[1] if len(item) > 1 else "Cơ bản"
            title = item[2] if len(item) > 2 else ""
            desc = item[3] if len(item) > 3 else ""
            starter = item[4] if len(item) > 4 else ""
            tests = item[5] if len(item) > 5 else []
            
            # Chuẩn hóa test cases
            formatted_tests = []
            if isinstance(tests, list):
                for t in tests:
                    if isinstance(t, dict):
                        formatted_tests.append(t)
                    elif isinstance(t, tuple) and len(t) >= 2:
                        formatted_tests.append({"input": str(t[0]), "expected_output": str(t[1])})
            if not formatted_tests:
                formatted_tests = [{"input": "0", "expected_output": ""}]

            concept = map_exercise_to_concept(ex_id, title, desc)

            standardized_list.append({
                "id": ex_id,
                "level": level,
                "title": f"[{level}] {title}",
                "concept_id": concept,
                "chapter": f"Chủ đề {ex_id.split('_')[0] if '_' in ex_id else 'Cốt lõi'}",
                "description": desc,
                "starter_code": starter,
                "test_cases": formatted_tests
            })
        elif isinstance(item, dict):
            if "concept_id" not in item:
                item["concept_id"] = map_exercise_to_concept(
                    item.get("id", ""), 
                    item.get("title", ""), 
                    item.get("description", "")
                )
            standardized_list.append(item)

    return standardized_list