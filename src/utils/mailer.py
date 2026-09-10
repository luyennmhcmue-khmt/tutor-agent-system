import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_real_otp_email(to_email: str, otp_code: str) -> tuple[bool, str]:
    """
    Gửi mã OTP thật về hộp thư Gmail của người dùng qua giao thức SMTP SSL (Cổng 465).
    """
    smtp_user = os.getenv("SMTP_EMAIL", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip().replace(" ", "")

    if not smtp_user or not smtp_pass:
        return False, "Hệ thống chưa cấu hình SMTP_EMAIL hoặc SMTP_PASSWORD (Mật khẩu ứng dụng Gmail) trong file .env."

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"EduCoder 10 <{smtp_user}>"
        msg["To"] = to_email
        msg["Subject"] = f"[{otp_code}] Mã xác thực khôi phục mật khẩu - EduCoder 10"

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto; padding: 25px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <h2 style="color: #0074A6; margin-top: 0;">EduCoder 10 - Khôi Phục Mật Khẩu</h2>
            <p>Chào Thầy/Cô và các bạn học sinh,</p>
            <p>Hệ thống nhận được yêu cầu đặt lại mật khẩu cho tài khoản liên kết với địa chỉ email này.</p>
            <div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; text-align: center; margin: 20px 0;">
                <span style="font-size: 28px; font-weight: bold; letter-spacing: 6px; color: #0f172a;">{otp_code}</span>
            </div>
            <p style="font-size: 13px; color: #64748b;">Mã OTP có hiệu lực trong vòng <b>5 phút</b>. Vui lòng không chia sẻ mã này cho bất kỳ ai.</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
            <p style="font-size: 12px; color: #94a3b8; margin-bottom: 0;">Trân trọng,<br>Ban quản trị Hệ thống EduCoder 10</p>
        </div>
        """
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        return True, f"Mã OTP đã được gửi thành công đến hộp thư {to_email}!"
    except smtplib.SMTPAuthenticationError:
        return False, "Xác thực Gmail thất bại. Vui lòng kiểm tra lại Mật khẩu ứng dụng (App Password) trong .env."
    except Exception as e:
        return False, f"Lỗi kết nối máy chủ gửi mail: {str(e)}"