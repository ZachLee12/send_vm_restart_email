import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from simple_chalk import chalk


load_dotenv(override=True)

# EmailMessage config
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
# smartregion@hslu.ch

subject = "[SRL VM]"
template = f"""
VM Restarted.
"""
context = ssl.create_default_context()
email_message = EmailMessage()
email_message["From"] = sender_email
email_message["To"] = receiver_email
email_message["Subject"] = subject
email_message.set_content(template)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, os.getenv("EMAIL_PASSWORD", "default"))
        smtp.sendmail(sender_email, receiver_email, email_message.as_string())

        print(chalk.green("[Email]: Email sent successfully"))
except Exception as e:
    print(f"{chalk.red('Failed to send email.')}: {e}")

    
