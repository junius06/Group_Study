import smtplib
from email.mime.text import MIMEText

send_email = "joohee5079@naver.com"
send_pwd = "password"

recv_email = "joohee5079@naver.com"

smtp_name = "smtp.naver.com"
smtp_port = 587

text = """
This is test mail.
Hello World.
"""

msg = MIMEText(text)

msg['Subject'] = "TEST MAIL"
msg['From'] = send_email
msg['To'] = recv_email
print(msg.as_string())

s = smtplib.SMTP(smtp_name, smtp_port)
s.starttls()
s.login(send_email, send_pwd)
s.sendmail(send_email, recv_email, msg.as_string())
s.quit()