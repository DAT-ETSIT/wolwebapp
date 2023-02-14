import os
from cryptography.fernet import Fernet

scriptPath = os.path.realpath(os.path.dirname(__file__))

key = Fernet.generate_key()
cipher = Fernet(key)
cryptedPass = cipher.encrypt(os.environ.get('MAIL_PASS').encode())

with open('/root/.wolsimpleserverkey', 'wb') as f:
    f.write(key)

with open(f"{scriptPath}/secrets", 'wb') as f:
    f.write(cryptedPass)
