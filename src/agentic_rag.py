from typing import Dict, Any, List
from src.ast_engine import ASTAnalyzer
from src.graph import PedagogicalKnowledgeGraph

class GraphRAGRetriever:
    """
    Tác tử truy xuất đồ thị tri thức sư phạm kết hợp phân tích AST.
    """

    def __init__(self):
        self.pkg = PedagogicalKnowledgeGraph()

    def retrieve_pedagogical_context(self, current_concept: str, code_str: str) -> Dict[str, Any]:
        ast_info = ASTAnalyzer.analyze_code(code_str)
        prereqs = self.pkg.get_prerequisites(current_concept)
        misconceptions = self.pkg.get_misconceptions(current_concept)

        issues: List[str] = []
        if not ast_info["syntax_valid"]:
            issues.append(ast_info["error_msg"])

        if current_concept == "vong_lap_for":
            if ast_info["has_for"] and not ast_info["has_range"]:
                issues.append("Sử dụng vòng lặp for nhưng chưa dùng hàm sinh dãy range().")
        elif current_concept == "cau_lenh_if":
            if not ast_info["has_if"] and ast_info["syntax_valid"]:
                issues.append("Bài học yêu cầu cấu trúc rẽ nhánh nhưng chưa xuất hiện câu lệnh if.")

        return {
            "concept": current_concept,
            "ast_analysis": ast_info,
            "prerequisites": prereqs,
            "misconceptions": misconceptions,
            "detected_issues": issues
        }