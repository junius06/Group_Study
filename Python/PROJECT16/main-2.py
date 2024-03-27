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
