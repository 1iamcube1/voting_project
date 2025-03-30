import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(to, subject, text):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, to, msg.as_string())
    server.quit()