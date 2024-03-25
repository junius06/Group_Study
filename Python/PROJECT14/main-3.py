import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart


send_email = "joohee5079@naver.com"
send_pwd = "password"

recv_email = "joohee6218@gmail.com"

msg = MIMEMultipart()

msg['Subject'] = "TEST MAIL"
msg['From'] = send_email
msg['To'] = recv_email
msg['Date'] = formatdate(localtime=True)

html_body = """
<html>
    <body>
        <h1>링크 확인. <a href="https://naver.com">네이버</a></h1>
    </body>
</html>
<p>&nbsp;</p>
<h3> TITLE </h3>
<p>Table</p>
<table style="height: 80px;" width="241">
<tbody>
<tr>
<td style="width: 70px;">1</td>
</tr>
</tbody>
</table>
"""

msg.attach(MIMEText(html_body, 'html'))

mailServer = smtplib.SMTP_SSL('smtp.naver.com')
mailServer.login(send_email, send_pwd)
# mailServer.send_message(msg)
mailServer.sendmail(send_email, recv_email, msg.as_string())
mailServer.quit()