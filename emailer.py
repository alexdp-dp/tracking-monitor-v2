import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText


load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = [email.strip() for email in os.getenv("EMAIL_TO").split(",")]


def send_email(subject, body):

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = EMAIL_FROM
    message["To"] = ", ".join(EMAIL_TO)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

        smtp.starttls()

        smtp.login(
            EMAIL_FROM,
            EMAIL_PASSWORD
        )

        smtp.sendmail(
            EMAIL_FROM,
            EMAIL_TO,
            message.as_string()
        )

