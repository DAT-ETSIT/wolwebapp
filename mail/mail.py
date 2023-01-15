from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

try:
    import mail.mailConfig as config
except:
    print("No se ha definido un fichero de configuración para el envío de correo.")

def sendMail(to, subject, message):
    try:
        config
    except:
        return 1

    if (message is None):
        print("Error")
        return 2

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
        with open(f'{os.path.dirname(__file__)}/templates/{template}.html') as f:
            content = f.read()
            for field in fields.keys():
                content = content.replace(field, fields[field])

            return content
    except:
        print("Fallo al generar el mensaje.")
        return None