# 🌱 OtpMint v1.0.0-beta

OtpMint is a lightweight, self-hosted OTP service built with Flask and SQLite3.
It lets you mint OTPs, send them via email using your own SMTP credentials, and verify them securely with attempt limiting.

No SaaS.
No third-party auth providers.
You own the keys, the mail server, and the data.
Everything is customizeable/changeable.

---

## ✨ Features

- Generates secure 6-digit OTPs
- Sends OTPs via SMTP email
- Never exposes OTPs directly
- Stores only hashed OTPs
- Limits verification attempts
- Developer mode for debugging
- SQLite backend (zero setup)

---

## 🧠 How It Works

1.You have to register an secret key via /reg_secretkey with your smtp server details. NOTE: The password is stored in plain text! Not recommended for production, change the logic if you want it to be more secure incase a db leak happens

2. Calling the `/otp` with recipient_mail (customer mail) your secret key will send a mail with the otp, return a shareableKey and adds the hashed otp to the database on sucess.
   
3. Now, when the customer/user enters the OTP you have to call `/verify-otp` with the shareableKey and whatever they entered as the otp. If it matches, it returns the status code 201. 

---

## 📦 Project Structure

OtpMint/
- main.py            Main Fask App
- generatives.py     OTP generation and email logic
- db.py              SQLite database access layer
- developer_mode.py  Developer / production switch
- map.db             SQLite database

---

## 🔧 Installation

### 1. Clone the repository

git clone https://github.com/creaminitalt/otpmint
cd otpmint

### 2. Install dependencies

pip install flask flask-limiter

### 3. Run the server

python main.py

Server runs at:
http://127.0.0.1:5000

---

## 🔑 Developer Mode

Edit developer_mode.py:

developer_mode = True

True  -> verbose internal errors (development only) ⚠️ Do not use in production
False -> safe generic errors (recommended for production)

---

## 📡 API Reference

### Register a secretKey

POST /reg_secretkey

{
  "secretKey": "my_app_key", #Random Strings Recommended
  "smtp_host": "smtp.example.com",
  "smtp_port": 587,
  "smtp_mail": "no-reply@example.com",
  "smtp_password": "email_password"
}

Response:
Registration of secretKey succeeded.

---

### Request OTP

POST /otp

{
  "mail": "user@example.com", # Recipient Mail
  "secretKey": "my_app_key"
}

Response:
AbCDeFgHiJ

This is the shareableKey, not the OTP.

---

### Verify OTP

POST /verify-otp

{
  "shareableKey": "AbCDeFgHiJ",
  "otp": "123456"
}

Responses:
201  OTP verified  
403  OTP mismatch  
400  Blocked or invalid key  
500  Internal error  

---

## 🛡️ Security Notes

- OTPs are hashed before storage
- OTPs are single-use
- Verification attempts are limited
- No third-party authentication services involved

Not included by default:
- OTP expiration by time
- Distributed rate limiting
- Encryption at rest

---

## 🧑‍💻 Developer's notes
This project might have many security vulnerbilities, but modify them as much as you want to fix,
I personally recommend you to not store passwords as plain text...
Some good changes are:
- OTP Expiration
- Randomized salt
- Change flask-limiter storage uri to smth else
- Migrate from sqlite3 (For big projects)
- Async / Connection pooling for the db
- Any other security measures
Customize as much as you want :)

This was an hooby project consider taking security measures before you use it for something big! Right now this is enough for simple applications.
The next version will include more channels other than mailing like telegram,etc...
