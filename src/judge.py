import os
import sys
import subprocess
import json
import re
import tempfile
import unicodedata

def extract_numbers(text: str) -> list[float]:
    """Trích xuất tất cả các số thực hoặc số nguyên có trong văn bản."""
    raw_nums = re.findall(r"[-+]?\d*\.?\d+", text)
    nums = []
    for n in raw_nums:
        if n not in ["-", "+", "", "."]:
            try:
                nums.append(float(n))
            except ValueError:
                pass
    return nums

def numbers_match(actual_nums: list[float], expected_nums: list[float]) -> bool:
    """So sánh dãy số học: Chấp nhận học sinh in kèm lời dẫn hoặc câu nhắc."""
    if not expected_nums:
        return False
    if len(actual_nums) == len(expected_nums):
        return all(abs(a - e) < 1e-3 for a, e in zip(actual_nums, expected_nums))
    if len(actual_nums) >= len(expected_nums):
        tail = actual_nums[-len(expected_nums):]
        if all(abs(a - e) < 1e-3 for a, e in zip(tail, expected_nums)):
            return True
    return False

def grade_code(student_code: str, test_cases) -> dict:
    """
    Hệ thống chấm mã nguồn đa tiêu chí:
    - Chấm độc lập từng Test Case: Làm đúng bao nhiêu test thì tính bấy nhiêu điểm trên thang 10.
    - So khớp đa tầng: So khớp dãy số học, so khớp chuỗi ký tự, loại bỏ nhiễu từ câu nhắc input.
    """
    if not student_code or not student_code.strip():
        return {
            "score": 0.0, "passed": 0, "total": 0,
            "status": "Chưa có mã nguồn", "verdict": "WA",
            "details": "⚠️ Bạn chưa nhập mã nguồn vào trình soạn thảo.", "failed_line": None
        }

    # Chuẩn hóa danh sách test case
    if isinstance(test_cases, str):
        try:
            test_cases = json.loads(test_cases)
        except Exception:
            test_cases = []

    if not test_cases:
        test_cases = [{"input": "", "output": "Xin chào"}]

    total_tests = len(test_cases)
    passed_count = 0
    test_results = []
    failed_line = None
    has_rte = False

    # Chèn cờ ép buộc UTF-8 chuẩn trên hệ điều hành Windows
    wrapped_code = (
        "import sys\n"
        "if hasattr(sys.stdout, 'reconfigure'):\n"
        "    sys.stdout.reconfigure(encoding='utf-8', errors='replace')\n"
        "if hasattr(sys.stderr, 'reconfigure'):\n"
        "    sys.stderr.reconfigure(encoding='utf-8', errors='replace')\n"
    ) + student_code

    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".py", delete=False) as f:
            f.write(wrapped_code)
            temp_file = f.name
    except Exception as e:
        return {
            "score": 0.0, "passed": 0, "total": total_tests,
            "status": "Runtime Error (RTE)", "verdict": "RTE",
            "details": f"Lỗi khởi tạo tệp thực thi: {str(e)}", "failed_line": None
        }

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        for idx, tc in enumerate(test_cases, 1):
            if not isinstance(tc, dict):
                continue

            inp = str(tc.get("input", ""))
            expected = str(tc.get("output", "")).strip()

            try:
                proc = subprocess.run(
                    [sys.executable, "-X", "utf8", temp_file],
                    input=inp.encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=3.0,
                    env=env
                )

                stdout_str = (proc.stdout or b"").decode("utf-8", errors="replace").strip()
                stderr_str = (proc.stderr or b"").decode("utf-8", errors="replace").strip()

                # Bắt lỗi cú pháp hoặc lỗi thực thi (Runtime Error)
                if proc.returncode != 0:
                    has_rte = True
                    err_lines = stderr_str.strip().splitlines()
                    last_err = err_lines[-1] if err_lines else "Lỗi thực thi không xác định"
                    line_matches = re.findall(r'line (\d+)', stderr_str)
                    if line_matches:
                        failed_line = max(1, int(line_matches[-1]) - 4)

                    test_results.append(f"Test #{idx} (Input: '{inp}'): ❌ Lỗi thực thi -> {last_err}")
                    continue

                # Chuẩn hóa Unicode NFC đối soát kết quả
                norm_actual = unicodedata.normalize("NFC", stdout_str.replace("\r\n", "\n").strip())
                norm_expected = unicodedata.normalize("NFC", expected.replace("\r\n", "\n").strip())

                exp_nums = extract_numbers(norm_expected)
                act_nums = extract_numbers(norm_actual)

                is_pass = False
                # 1. So khớp bằng giá trị số học
                if exp_nums and numbers_match(act_nums, exp_nums):
                    is_pass = True
                # 2. So khớp bằng chuỗi ký tự chuẩn hóa
                elif norm_actual == norm_expected:
                    is_pass = True
                elif norm_expected.lower() in norm_actual.lower():
                    is_pass = True

                if is_pass:
                    passed_count += 1
                    test_results.append(f"Test #{idx} (Input: '{inp}'): ✅ ĐẠT (Khớp kết quả '{expected}')")
                else:
                    test_results.append(f"Test #{idx} (Input: '{inp}'): ❌ SAI (Đầu ra: '{stdout_str}' | Kỳ vọng: '{expected}')")

            except subprocess.TimeoutExpired:
                test_results.append(f"Test #{idx}: ⏰ Quá thời gian quy định (> 3.0 giây - TLE)")
            except Exception as e:
                test_results.append(f"Test #{idx}: ❌ Lỗi hệ thống: {str(e)}")

    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

    # Tính điểm: Học sinh làm đúng bao nhiêu test thì hưởng bấy nhiêu phần trăm thang điểm 10
    final_score = round((passed_count / total_tests) * 10.0, 1) if total_tests > 0 else 0.0

    if passed_count == total_tests and total_tests > 0:
        verdict = "AC"
        status_label = f"Accepted (AC) - Đạt {passed_count}/{total_tests} Tests"
    elif has_rte and passed_count == 0:
        verdict = "RTE"
        status_label = f"Runtime Error (RTE) - 0/{total_tests} Tests"
    else:
        verdict = "WA"
        status_label = f"Đạt {passed_count}/{total_tests} Tests ({final_score}/10 Điểm)"

    return {
        "score": final_score,
        "passed": passed_count,
        "total": total_tests,
        "status": status_label,
        "verdict": verdict,
        "details": "\n".join(test_results),
        "failed_line": failed_line
    }

run_isolated_judge = grade_code