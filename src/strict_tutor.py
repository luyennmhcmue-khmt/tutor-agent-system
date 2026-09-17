# src/strict_tutor.py
import re
from typing import Dict, Any

# Bộ lọc cưỡng bức loại bỏ 100% từ phỏng đoán/thiếu kiên định
BANNED_WORDS = [
    r"\bcó thể\b", r"\bcó lẽ\b", r"\bdường như\b", 
    r"\bhình như\b", r"\bchắc là\b", r"\bđoán là\b"
]

def purge_hedging(text: str) -> str:
    """Thay thế triệt để các từ ức đoán bằng văn phong chuẩn mực sư phạm."""
    result = text
    for pattern in BANNED_WORDS:
        result = re.sub(pattern, "bắt buộc", result, flags=re.IGNORECASE)
    return result.strip()

# Tri thức chuẩn từ Hộp kiến thức 170 trang SGK Tin học 10 KNTT
SGK_RULES = {
    "type_cast": {
        "bai": "Bài 18: Các lệnh vào ra đơn giản (Trang 97 - 100)",
        "quy_tac": "Lệnh input() luôn trả về dữ liệu kiểu xâu kí tự (str). Để tính toán số học, bắt buộc dùng hàm ép kiểu int() hoặc float().",
        "cu_phap": "<tên_biến> = int(input(\"Dòng nhắc\"))\n<tên_biến> = float(input(\"Dòng nhắc\"))",
        "cau_hoi": "Lệnh input() trả về kiểu dữ liệu gì? Cần dùng hàm nào bao ngoài input() để thực hiện phép tính cộng số học?"
    },
    "operator_assign": {
        "bai": "Bài 17 & 19: Biến, lệnh gán và câu lệnh rẽ nhánh (Trang 91, 101)",
        "quy_tac": "Dấu '=' là lệnh gán giá trị. Phép so sánh bằng trong mệnh đề điều kiện bắt buộc dùng cặp dấu '=='.",
        "cu_phap": "if <biến> == <giá_trị>:\n    <khối_lệnh>",
        "cau_hoi": "Trong câu lệnh điều kiện if, ký hiệu nào dùng để so sánh bằng thay cho lệnh gán giá trị?"
    },
    "syntax_colon": {
        "bai": "Bài 19 & 20: Câu lệnh rẽ nhánh và lặp (Trang 101, 105)",
        "quy_tac": "Cuối các dòng lệnh if, else, elif, for, while bắt buộc phải có dấu hai chấm (:). Khối lệnh con thụt lề 4 dấu cách.",
        "cu_phap": "if <điều_kiện>:\n    <lệnh_thực_thi>\nelse:\n    <lệnh_thực_thi>",
        "cau_hoi": "Dòng lệnh điều khiển đang thiếu ký tự kết thúc bắt buộc nào theo quy định của Python?"
    },
    "indentation_error": {
        "bai": "Bài 19: Câu lệnh rẽ nhánh if (Trang 102)",
        "quy_tac": "Các lệnh trong cùng một khối bắt buộc phải thụt lề thống nhất đúng 4 dấu cách (1 tab).",
        "cu_phap": "<lệnh_chính>:\n    <lệnh_con_thụt_lề_4_cách>",
        "cau_hoi": "Khối lệnh bên trong mệnh đề điều khiển đã được thụt lề thống nhất 4 dấu cách chưa?"
    },
    "loop_while": {
        "bai": "Bài 21: Câu lệnh lặp while (Trang 108 - 110)",
        "quy_tac": "Vòng lặp while lặp lại chừng nào điều kiện còn đúng. Trong thân vòng lặp bắt buộc có câu lệnh cập nhật biến lặp để tránh lặp vô hạn.",
        "cu_phap": "while <điều_kiện>:\n    <khối_lệnh>\n    <cập_nhật_biến_lặp>",
        "cau_hoi": "Biến điều khiển vòng lặp đã được cập nhật giá trị ở cuối mỗi vòng lặp để tạo điểm dừng chưa?"
    }
}

def format_socratic_response(tag: str, line_number: int = None, attempt: int = 1) -> Dict[str, str]:
    """
    Sinh phản hồi trực diện:
    - Đúng trọng tâm lỗi
    - Trích xuất căn cứ SGK
    - Gợi mở tư duy không lan man
    - Xuất cú pháp chuẩn mực
    """
    rule = SGK_RULES.get(tag, {
        "bai": "SGK Tin học 10 (Bộ Kết nối tri thức với cuộc sống)",
        "quy_tac": "Mã nguồn vi phạm quy chuẩn cú pháp Python chuẩn mực.",
        "cu_phap": "# Kiểm tra lại cấu trúc câu lệnh theo SGK",
        "cau_hoi": "Đối chiếu lại cấu trúc dòng lệnh với ví dụ mẫu trong bài học SGK."
    })

    line_info = f"tại dòng {line_number}" if line_number else "trong đoạn mã"

    diem_sai = f"Lỗi cú pháp {line_info}: Vi phạm quy tắc cấu trúc lệnh Python."
    can_cu = f"{rule['quy_tac']} (Căn cứ: {rule['bai']})."
    
    # Lần 1: Dẫn dắt bằng câu hỏi ngắn. Lần 2 trở đi: Yêu cầu đối soát cú pháp trực tiếp.
    goi_y = rule["cau_hoi"] if attempt == 1 else "Áp dụng chính xác cú pháp quy chuẩn dưới đây để sửa lỗi:"

    return {
        "diem_sai": purge_hedging(diem_sai),
        "can_cu_sgk": purge_hedging(can_cu),
        "dinh_huong": purge_hedging(goi_y),
        "cu_phap_chuan": rule["cu_phap"]
    }