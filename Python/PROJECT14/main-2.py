import os
import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
# from email.header import Header
from email.mime.multipart import MIMEMultipart
from getpass import getpass

send_email = "joohee5079@naver.com"
send_pwd = getpass("Enter pwd: ")

recv_email = "joohee5079@naver.com"

msg = MIMEMultipart()

msg['Subject'] = "TEST MAIL"
msg['From'] = send_email
msg['To'] = recv_email
msg['Date'] = formatdate(localtime=True)
body = MIMEText('첨부파일 2개 있음.', _charset='utf-8')
msg.attach(body)

files = ['./results/main-1.png', './results/main-2.png']

for i in files:
    if os.path.exists(i):
        with open(i, "rb") as file:  # Ensure file is properly closed after being read
            part = MIMEBase('application', "octet-stream")
            part.set_payload(file.read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(i))
        msg.attach(part)
    else:
        print(f"File not found: {i}")  # 파일이 없는 경우 경고 출력

mailServer = smtplib.SMTP_SSL('smtp.naver.com')
mailServer.login(send_email, send_pwd)
mailServer.send_message(msg)
mailServer.quit()