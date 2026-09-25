import networkx as nx
from typing import List, Dict, Any

class PedagogicalKnowledgeGraph:
    """
    Đồ thị tri thức sư phạm chuẩn hóa theo SGK Tin học 10 (Bộ sách Kết nối tri thức).
    Thể hiện quan hệ tiên quyết (PREREQUISITE_OF) và lỗi quan niệm sai (HAS_MISCONCEPTION).
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        concepts = [
            ("bien_va_kieu_du_lieu", {"name": "Biến và kiểu dữ liệu cơ bản", "unit": 14}),
            ("bieu_thuc_logic", {"name": "Biểu thức điều kiện và logic", "unit": 15}),
            ("cau_lenh_if", {"name": "Cấu trúc rẽ nhánh if-else", "unit": 16}),
            ("ham_range", {"name": "Hàm range() sinh dãy số", "unit": 17}),
            ("vong_lap_for", {"name": "Cấu trúc lặp for", "unit": 17}),
            ("vong_lap_while", {"name": "Cấu trúc lặp while", "unit": 18}),
            ("kieu_du_lieu_xau", {"name": "Xử lý xâu ký tự (String)", "unit": 19}),
            ("kieu_du_lieu_danh_sach", {"name": "Danh sách (List)", "unit": 20}),
            ("ham_tu_dinh_nghia", {"name": "Hàm tự định nghĩa (def)", "unit": 26}),
            ("bien_va_kieu_du_lieu", {"name": "Biến và kiểu dữ liệu cơ bản", "unit": 14}),
            ("bieu_thuc_logic", {"name": "Biểu thức điều kiện và logic", "unit": 15}),
            ("cau_lenh_if", {"name": "Cấu trúc rẽ nhánh if-else", "unit": 16}),
            ("ham_range", {"name": "Hàm range() sinh dãy số", "unit": 17}),
            ("vong_lap_for", {"name": "Cấu trúc lặp for", "unit": 17}),
            ("vong_lap_while", {"name": "Cấu trúc lặp while", "unit": 18}),
            ("kieu_du_lieu_xau", {"name": "Xử lý xâu ký tự (String)", "unit": 19}),
            ("kieu_du_lieu_danh_sach", {"name": "Danh sách & Mảng một chiều (List)", "unit": 20}),
            ("thuat_toan_tim_kiem", {"name": "Thuật toán tìm kiếm (Tuyến tính / Nhị phân)", "unit": 22}),
            ("thuat_toan_sap_xep", {"name": "Thuật toán sắp xếp (Bubble / Selection Sort)", "unit": 23}),
        ]
        self.graph.add_nodes_from(concepts)

        prerequisites = [
            ("bien_va_kieu_du_lieu", "bieu_thuc_logic"),
            ("bieu_thuc_logic", "cau_lenh_if"),
            ("bien_va_kieu_du_lieu", "ham_range"),
            ("ham_range", "vong_lap_for"),
            ("bieu_thuc_logic", "vong_lap_while"),
            ("vong_lap_for", "kieu_du_lieu_xau"),
            ("vong_lap_for", "kieu_du_lieu_danh_sach"),
            ("cau_lenh_if", "ham_tu_dinh_nghia"),
            ("vong_lap_for", "ham_tu_dinh_nghia"),
            ("kieu_du_lieu_danh_sach", "thuat_toan_tim_kiem"),
            ("kieu_du_lieu_danh_sach", "thuat_toan_sap_xep"),
            ("vong_lap_for", "thuat_toan_sap_xep"),
        ]
        for src, dst in prerequisites:
            self.graph.add_edge(src, dst, relation="PREREQUISITE_OF")

        misconceptions = [
            ("misc_range_bound", "Nhầm biên range(n) chạy từ 1..n thay vì 0..n-1"),
            ("misc_indentation", "Thiếu thụt lề 4 dấu cách sau dấu hai chấm :"),
            ("misc_assign_vs_equal", "Dùng dấu = (gán) thay vì == (so sánh bằng) trong mệnh đề if"),
            ("misc_infinite_while", "Quên tăng/giảm biến đếm dẫn đến vòng lặp vô tận trong while"),
            ("misc_list_index", "Truy cập phần tử vượt quá chỉ số (IndexError)"),
        ]
        for m_id, desc in misconceptions:
            self.graph.add_node(m_id, description=desc, node_type="misconception")

        self.graph.add_edge("ham_range", "misc_range_bound", relation="HAS_MISCONCEPTION")
        self.graph.add_edge("cau_lenh_if", "misc_indentation", relation="HAS_MISCONCEPTION")
        self.graph.add_edge("cau_lenh_if", "misc_assign_vs_equal", relation="HAS_MISCONCEPTION")
        self.graph.add_edge("vong_lap_for", "misc_indentation", relation="HAS_MISCONCEPTION")
        self.graph.add_edge("vong_lap_while", "misc_infinite_while", relation="HAS_MISCONCEPTION")
        self.graph.add_edge("kieu_du_lieu_danh_sach", "misc_list_index", relation="HAS_MISCONCEPTION")

    def get_prerequisites(self, concept_id: str) -> List[str]:
        if concept_id not in self.graph:
            return []
        return [
            pred for pred, _, data in self.graph.in_edges(concept_id, data=True)
            if data.get("relation") == "PREREQUISITE_OF"
        ]

    def get_misconceptions(self, concept_id: str) -> List[Dict[str, str]]:
        if concept_id not in self.graph:
            return []
        results = []
        for _, succ, data in self.graph.out_edges(concept_id, data=True):
            if data.get("relation") == "HAS_MISCONCEPTION":
                desc = self.graph.nodes[succ].get("description", "")
                results.append({"id": succ, "description": desc})
        return results