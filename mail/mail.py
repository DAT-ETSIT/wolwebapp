from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import config

def sendMail(to, subject, message):
    if (message is None):
        print("Error")
        return 1

    msg = MIMEMultipart()

    msg['From'] =  f'{config.mailName} <{config.mailUser}>'
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))
    
    server = smtplib.SMTP(f'{config.mailServer}:{config.mailPort}')
    server.starttls()
    server.login(config.mailUser, config.mailPass)
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    return 0

def buildMessage(template, fields = {}):
    try:
        with open(f'./templates/{template}.html') as f:
            content = f.read()
            for field in fields.keys():
                content = content.replace(field, fields[field])

            return content
    except:
        return None