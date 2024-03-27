import imaplib
import email
from email import policy
from getpass import getpass

def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    subject, encode = info[0]
    return subject, encode

imap = imaplib.IMAP4_SSL('imap.naver.com')
id = 'joohee5079@naver.com'
pw = getpass("Enter pwd: ")
imap.login(id, pw)

imap.select('INBOX')
resp, data = imap.uid('search', None, 'All')
all_email = data[0].split()
last_email = all_email[-5:]

for mail in reversed(last_email):
    # fetch 명령어를 이용해 특정 이메일을 가져오고, 변수 mail은 이메일의 고유 ID이며, RFC822 포맷을 요청하여 이메일의 전체 텍스트(헤더, 본문 등)를 가져온다.
    result, data = imap.uid('fetch', mail, '(RFC822)') 
    # data[0]은 이메일 인코딩된 데이터를 파싱해온 값인 것 같다. data[1]은 이메일 주소의 UID같다.
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email, policy=policy.default)

    print('='*70)
    print('FROM:', email_message['From'])
    print('SENDER:', email_message['Sender'])
    print('TO:', email_message['To'])
    print('DATE:', email_message['Date'])
    subject, encode = find_encoding_info(email_message['Subject'])
    print('SUBJECT:', subject)
    print('='*70)
    
imap.close()
imap.logout()