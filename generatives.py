import hashlib
import string
import random
import secrets
import smtplib
from email.message import EmailMessage

from db import *
import developer_mode

DEVELOPER_MODE = developer_mode.state()



def mail(recipient_mail,secretKey,otp):
    try:
        response = getfrom_secretKey(secretKey)
        if response[1] == 2000:
            row,status = response
        _secretKey, smtp_host, smtp_port, smtp_mail, smtp_password = row
        msg = EmailMessage()
        msg["From"] = smtp_mail
        msg["To"] = recipient_mail
        msg["Subject"] = "One Time Password"
        msg.set_content(otp)

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as serv:
                serv.login(smtp_mail, smtp_password)
                serv.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as serv:
                serv.starttls()
                serv.login(smtp_mail, smtp_password)
                serv.send_message(msg)
        print("Mail Sent Sucessfully!")
        return "Operation Completed Sucessfully", 2000
    except Exception as e:
        print("Error Mail Sender ", e)
        if not DEVELOPER_MODE:
            return "Unknown Error", 6002
        return f"Unknown Error - {e}", 6002
    

def OTP(recipient_mail,secretKey):
    try:
        otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
        hashed = hasher(otp)
        kix = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        rspm = mail(recipient_mail,secretKey,otp)
        if not rspm[1] == 2000:
            return "Mail Error", 6055
        rsp = add_data(kix,hashed)
        rsp2 = add_blocklist(kix,0)
        if not rsp[1] == 2000:
            return rsp
        return kix, 2000
    except Exception as e:
        return f"Unknown error - {e}", 6001


def hasher(data):
    salt = "addanysalthereipreferkanye" # Optionally, dont hardcode salt like this. Try a better logic or smth lol :)
    data = salt + data
    hagent = hashlib.sha256(data.encode()).hexdigest()
    return hagent
