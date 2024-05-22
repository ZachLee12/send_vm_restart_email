import smtplib
import sys
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def sendMail(credentials, recipients, cc, bcc, subject, plain, html, attachments):
    errorMsg = ''
    old_stderr = sys.stderr
    sys.stderr = open('/home/smartregionadmin/reporter/py/logs/mail.log', 'a')
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = credentials['sender']
    msg['To'] = ', '.join(recipients)
    msg['Cc'] = ', '.join(cc)
    msg['Bcc'] = ', '.join(bcc)

    #mail body
    #msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html, 'html'))


    #attachments
    for f in attachments or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(),Name=basename(f))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    try:
        smtpObj = smtplib.SMTP(credentials['server'], credentials['port'])
        smtpObj.set_debuglevel(2)
        smtpObj.starttls()
        smtpObj.login(credentials['sender'], credentials['password'])
        smtpObj.send_message(msg)
    except:
        errorMsg  = str(sys.exc_info())
        logging.error(sys.exc_info())
    if smtpObj:
        smtpObj.quit()
    sys.stderr = old_stderr
    return errorMsg




