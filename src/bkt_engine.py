class DynamicKnowledgeTracing:
    """
    Thuật toán Bayesian Knowledge Tracing (BKT) chuẩn hóa:
    - P(L0): Xác suất nắm vững ban đầu
    - P(T):  Xác suất tiếp thu kiến thức qua một lượt luyện tập
    - P(S):  Xác suất sơ suất / lơ đễnh (Slip)
    - P(G):  Xác suất đoán mò (Guess)
    """

    def __init__(
        self,
        p_l0: float = 0.35,
        p_trans: float = 0.20,
        p_slip: float = 0.10,
        p_guess: float = 0.20
    ):
        self.p_l0 = p_l0
        self.p_trans = p_trans
        self.p_slip = p_slip
        self.p_guess = p_guess

    def update_mastery(self, prior_mastery: float, is_correct: bool) -> float:
        """
        Cập nhật độ thành thạo kiến thức P(L_t+1) dựa trên quan sát (đúng/sai).
        """
        try:
            p_l = float(prior_mastery)
        except Exception:
            p_l = 0.5
        p_l = max(0.01, min(0.99, p_l))

        if is_correct:
            numerator = p_l * (1.0 - self.p_slip)
            denominator = numerator + ((1.0 - p_l) * self.p_guess)
        else:
            numerator = p_l * self.p_slip
            denominator = numerator + ((1.0 - p_l) * (1.0 - self.p_guess))

        p_l_given_obs = numerator / denominator if denominator != 0 else p_l
        next_mastery = p_l_given_obs + ((1.0 - p_l_given_obs) * self.p_trans)
        return round(max(0.05, min(0.98, next_mastery)), 4)

    def determine_scaffolding_level(
        self,
        mastery_score: float,
        syntax_valid: bool = True
    ) -> int:
        """
        Xác định cấp độ giàn giáo sư phạm (Scaffolding Level):
        - Cấp 1 (Mastery >= 0.75): Gợi ý phản tư cấp cao.
        - Cấp 2 (0.4 <= Mastery < 0.75): Chia nhỏ thuật toán theo 3 pha I-P-O.
        - Cấp 3 (Mastery < 0.4 hoặc Cú pháp lỗi): Chỉ rõ dòng lỗi và quy tắc ngữ nghĩa.
        """
        try:
            m = float(mastery_score)
        except Exception:
            m = 0.5

        if not syntax_valid or m < 0.40:
            return 3
        elif m < 0.75:
            return 2
        else:
            return 1