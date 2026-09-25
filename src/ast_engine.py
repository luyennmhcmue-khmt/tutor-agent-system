import ast
import sys
from typing import Dict, Any, List

class ASTAnalyzer:
    """
    Bộ phân tích cú pháp tĩnh AST cho chương trình Tin học 10 (Python 3):
    - Kiểm tra tính hợp lệ của cú pháp (Syntax Validity).
    - Trích xuất dòng và cột gây lỗi cụ thể.
    - Phát hiện các mẫu tư duy lập trình và lỗi phổ biến của học sinh lớp 10.
    """

    def __init__(self):
        pass

    def analyze(self, code: str) -> Dict[str, Any]:
        """Phân tích toàn diện mã nguồn của học sinh."""
        if not code or not code.strip():
            return {
                "syntax_valid": True,
                "is_empty": True,
                "error_msg": "Học sinh chưa viết mã nguồn.",
                "error_line": None,
                "error_col": None,
                "used_nodes": [],
                "detected_patterns": [],
                "summary": "Chưa có mã nguồn để phân tích."
            }

        # 1. Kiểm tra lỗi cú pháp (Syntax Error)
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "is_empty": False,
                "error_msg": e.msg,
                "error_line": e.lineno,
                "error_col": e.offset,
                "error_text": e.text.strip() if e.text else "",
                "used_nodes": [],
                "detected_patterns": ["syntax_error"],
                "summary": f"Lỗi cú pháp tại dòng {e.lineno}: '{e.msg}'"
            }

        # 2. Quét cấu trúc cú pháp nếu code hợp lệ
        visitor = CodeStructureVisitor()
        visitor.visit(tree)

        detected_patterns = []
        
        # Bẫy phổ biến 1: Dùng input() nhưng quên ép kiểu số int/float khi tính toán
        if visitor.has_input and not visitor.has_type_cast and (visitor.has_arithmetic or visitor.has_range):
            detected_patterns.append("missing_input_type_cast")

        # Bẫy phổ biến 2: Vòng lặp while True nhưng không có lệnh break
        if visitor.has_while_true and not visitor.has_break:
            detected_patterns.append("potential_infinite_loop")

        # Bẫy phổ biến 3: Cố tình gán lại ký tự của xâu s[i] = ...
        if visitor.has_subscript_assignment:
            detected_patterns.append("string_mutation_attempt")

        return {
            "syntax_valid": True,
            "is_empty": False,
            "error_msg": None,
            "error_line": None,
            "error_col": None,
            "used_nodes": list(visitor.node_types),
            "called_functions": list(visitor.called_functions),
            "variables": list(visitor.variables),
            "detected_patterns": detected_patterns,
            "has_loops": visitor.has_for or visitor.has_while,
            "has_conditions": visitor.has_if,
            "has_input": visitor.has_input,
            "has_print": visitor.has_print,
            "summary": "Cú pháp hợp lệ."
        }


class CodeStructureVisitor(ast.NodeVisitor):
    """Bộ duyệt cây AST để thu thập đặc trưng cú pháp."""

    def __init__(self):
        self.node_types = set()
        self.called_functions = set()
        self.variables = set()
        
        self.has_input = False
        self.has_print = False
        self.has_type_cast = False
        self.has_arithmetic = False
        self.has_range = False
        self.has_for = False
        self.has_while = False
        self.has_if = False
        self.has_while_true = False
        self.has_break = False
        self.has_subscript_assignment = False

    def generic_visit(self, node):
        self.node_types.add(type(node).__name__)
        super().generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            self.called_functions.add(func_name)
            if func_name == "input":
                self.has_input = True
            elif func_name == "print":
                self.has_print = True
            elif func_name in ("int", "float"):
                self.has_type_cast = True
            elif func_name == "range":
                self.has_range = True
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
            self.has_arithmetic = True
        self.generic_visit(node)

    def visit_For(self, node):
        self.has_for = True
        self.generic_visit(node)

    def visit_While(self, node):
        self.has_while = True
        # Kiểm tra while True:
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.has_while_true = True
        self.generic_visit(node)

    def visit_Break(self, node):
        self.has_break = True
        self.generic_visit(node)

    def visit_If(self, node):
        self.has_if = True
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
            elif isinstance(target, ast.Subscript):
                # Phát hiện dạng s[0] = 'a'
                self.has_subscript_assignment = True
        self.generic_visit(node)