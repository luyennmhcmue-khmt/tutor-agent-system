import smtplib
import random
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt
import streamlit as st
from src.db import get_connection

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def send_personalized_otp(email: str) -> tuple[bool, str]:
    email_clean = email.strip().lower()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_name, role FROM users WHERE LOWER(email) = ?", (email_clean,))
    user = cur.fetchone()
    
    if not user:
        conn.close()
        return False, "Địa chỉ Gmail này chưa được đăng ký trong hệ thống."

    full_name = user["full_name"]
    role = user["role"]
    otp_code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.now() + timedelta(minutes=3)

    cur.execute(
        "INSERT INTO password_otps (email, otp_code, role, expires_at) VALUES (?, ?, ?, ?)",
        (email_clean, otp_code, role, expires_at)
    )
    conn.commit()
    conn.close()

    # Mẫu thư cá nhân hóa theo vai trò
    if role == "teacher":
        salutation = f"Kính gửi Thầy/Cô {full_name},"
        sub_text = "Thầy/Cô vừa gửi yêu cầu đặt lại mật khẩu cho tài khoản Quản trị & Giảng dạy tại Educoder 10."
        caution = "Vì lý do an toàn học đường, toàn bộ phiên làm việc trên các thiết bị khác sẽ bị đăng xuất sau khi đổi mật khẩu."
    else:
        salutation = f"Chào em {full_name},"
        sub_text = "Hệ thống Educoder 10 nhận được yêu cầu đặt lại mật khẩu học tập của em."
        caution = "Mã xác nhận này chỉ dành riêng cho em, tuyệt đối không chia sẻ cho bạn bè."

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #0074A6; margin-top: 0;">Educoder 10 - Khôi Phục Mật Khẩu</h2>
        <p><b>{salutation}</b></p>
        <p>{sub_text}</p>
        <div style="background-color: #f8fafc; border: 1px dashed #0074A6; padding: 15px; border-radius: 6px; text-align: center; margin: 20px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0f172a;">{otp_code}</span>
        </div>
        <p style="color: #dc2626; font-size: 13px;"><b>Thời hạn hiệu lực: 3 phút</b> (sau 3 phút mã sẽ tự động vô hiệu hóa).</p>
        <p style="font-size: 13px; color: #64748b;">{caution}</p>
    </div>
    """

    try:
        smtp_user = st.secrets["SMTP_EMAIL"]
        smtp_pass = st.secrets["SMTP_PASSWORD"].replace(" ", "")
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Educoder 10 <{smtp_user}>"
        msg["To"] = email_clean
        msg["Subject"] = f"[{otp_code}] Mã xác thực khôi phục mật khẩu - Educoder 10"
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email_clean, msg.as_string())
        server.quit()
        return True, f"Mã xác thực đã được gửi về hộp thư {email_clean}."
    except Exception as e:
        return False, f"Lỗi máy chủ phát thư: {str(e)}"

def verify_and_reset_password(email: str, otp_entered: str, new_password: str) -> tuple[bool, str]:
    email_clean = email.strip().lower()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM password_otps 
        WHERE LOWER(email) = ? AND otp_code = ? AND is_used = 0 
        ORDER BY id DESC LIMIT 1
    """, (email_clean, otp_entered.strip()))
    record = cur.fetchone()

    if not record:
        conn.close()
        return False, "Mã OTP không chính xác hoặc đã qua sử dụng."

    expires_at = datetime.strptime(record["expires_at"], "%Y-%m-%d %H:%M:%S.%f")
    if datetime.now() > expires_at:
        conn.close()
        return False, "Mã OTP đã hết thời hạn hiệu lực (quá 3 phút). Vui lòng yêu cầu mã mới."

    # Cập nhật mật khẩu mới và đánh dấu đã dùng mã
    new_hash = hash_password(new_password)
    cur.execute("UPDATE users SET password_hash = ? WHERE LOWER(email) = ?", (new_hash, email_clean))
    cur.execute("UPDATE password_otps SET is_used = 1 WHERE id = ?", (record["id"],))
    conn.commit()
    conn.close()
    return True, "Cập nhật mật khẩu thành công!"