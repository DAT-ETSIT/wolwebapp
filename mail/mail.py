from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from cryptography.fernet import Fernet


try:
    import data.serverConfig as config
except:
    print("No se ha definido un fichero de configuración para el envío de correo.")

def getSecrets():
    scriptPath = os.path.realpath(os.path.dirname(__file__))

    with open('/root/.wolsimpleserverkey', 'rb') as f:
        key = f.read()
    cipher = Fernet(key)

    with open(f"{scriptPath}/secrets", 'rb') as f:
        cryptedPass = f.read()

    mailPass = cipher.decrypt(cryptedPass).decode()

    return mailPass

def sendMail(to, subject, message):
    try:
        config
    except:
        return 1

    if (message is None):
        print("No se ha definido un mensaje.")
        return 2

    mailUser, mailPass = getSecrets()

    msg = MIMEMultipart()

    try:
        mailPass = getSecrets()
    except:
        print("Error recuperando la clave del servidor de correo.")
        return 4

    msg['From'] =  f'{config.MAIL_NAME} <{mailPass}>'
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))
    
    server = smtplib.SMTP(f'{config.MAIL_SERVER}:{config.MAIL_PORT}')
    server.starttls()
    try:
        server.login(mailUser, mailPass)
    except:
        print("Error al iniciar sesión en el servidor.")
        return 3
    
    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    except:
        print("Error al enviar el mensaje.")
        return 4

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