import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from simple_chalk import chalk


load_dotenv(override=True)

# Config
config = {
    "SENDER_EMAIL": os.getenv("SENDER_EMAIL"),
    "RECEIVER_EMAIL": os.getenv("RECEIVER_EMAIL"),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
    "EMAIL_SERVER": os.getenv("EMAIL_SERVER"),
    "EMAIL_SERVER_PORT": os.getenv("EMAIL_SERVER_PORT"),
}

# Check if all .env variables are set
none_env_variables = [key for key in config.keys() if config.get(key) is None]
if len(none_env_variables) > 1:
    env_error_msg = ", ".join(none_env_variables) + " must be set in .env"
    raise ValueError(chalk.red(env_error_msg))


subject = "[SRL VM]"
template = f"""
VM Restarted.
"""
context = ssl.create_default_context()
email_message = EmailMessage()
email_message["From"] = config.get("SENDER_EMAIL")
email_message["To"] = config.get("RECEIVER_EMAIL")
email_message["Subject"] = subject
email_message.set_content(template)

try:
    with smtplib.SMTP_SSL(config.get("EMAIL_SERVER"), config.get("EMAIL_SERVER_PORT"), context=context) as smtp:
        smtp.login(config.get("SENDER_EMAIL"), config.get("EMAIL_PASSWORD"))
        smtp.sendmail(config.get("SENDER_EMAIL"), config.get("RECEIVER_EMAIL"), email_message.as_string())

        print(chalk.green("[Email]: Email sent successfully"))
except Exception as e:
    print(f"{chalk.red('Failed to send email. Reason:')} {e}")
