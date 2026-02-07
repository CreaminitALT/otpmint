#        SORRY FOR NOT ADDING CLASSESS AND STUFF I DIDNT WANT TO OVERCOMPLICATE

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from db import *
from generatives import *
import developer_mode

DEVELOPER_MODE = developer_mode.state()

def verify(ki,attempt):
    try:
        resp = get_val(ki)
        resp_data = resp[0]
        status_code = resp[1]
        if status_code == 2000:
            hashedotp = hasher(attempt)
            if hashedotp == resp_data:
                return "OTP Matched!", 1000
            else:
                return "OTP Mismatched!", 1001
        else:
            return resp, 1066
    except Exception as e:
        return e, 1067

app = Flask(__name__)
limit = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"],
    storage_uri="memory://"
)

@app.route("/otp", methods=["POST"])
def handle_otp():
    recipient_mail = request.json.get("mail")
    secretKey = request.json.get("secretKey")
    response = OTP(recipient_mail,secretKey)
    response_internal_statuscode = response[1]
    if not response_internal_statuscode == 2000:
        return f"Error: {response[0]} -- {response_internal_statuscode}", 400
    response = response[0]
    return response, 200

@app.route("/verify-otp", methods=["POST"])
def handle_verification():
    shareableKey = request.json.get("shareableKey")
    otp_attempt = request.json.get("otp")
    try:
        response = verify(shareableKey,otp_attempt)
        response_bl = modify_blocklist(shareableKey)
        thr_block = should_be_blocked(shareableKey)
        if thr_block == "err":
            return "Unknown Error in blocker"
        elif thr_block:
            return "Maximum Attempts Reached!", 400
        if response[1] == 1000:
            remove_data(shareableKey)
            remove_blocklist(shareableKey)
            return "OTP Matched!", 201
        elif response[1] == 1001:
            return "OTP Mismatched!", 403
        else:
            return response[0], 500
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 500
        else:
            return f"Unknown Error - {e}", 500

@app.route("/reg_secretkey", methods=["POST"])
def handle_registration_secretKey():
    try:
        secretKey = request.json.get("secretKey")
        smtp_host = request.json.get("smtp_host")
        smtp_port = request.json.get("smtp_port")
        smtp_mail = request.json.get("smtp_mail")
        smtp_pass = request.json.get("smtp_password")
    except Exception:
        return "Missing required fields", 400
    try:
        resp = register_secretKey(secretKey,smtp_host,smtp_port,smtp_mail,smtp_pass)
        if not resp[1] == 2000:
            return f"Unknown Error - Internal Error Code: {resp[1]}", 400
        return "Registration of secretKey succeeded."
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 400
        return f"Unknown Error - {e}", 400
        


app.run()