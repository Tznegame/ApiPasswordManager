import base64
import configparser
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class Security:
    def __init__(self):
        self.key = self.recoverKey()

    def recoverKey(self):
        psw = self.checkPassword(input("Inserisci la password \n"))
        password = psw.encode()  # Convert to type bytes
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    def encrypt(self, msg, key):
        message = msg.encode()
        f = Fernet(key)
        return f.encrypt(message).decode('utf-8')  # Encrypt the bytes. The returning object is of type bytes

    def decrypt(self, msg, key):
        message = msg.encode()
        f = Fernet(key)
        return f.decrypt(message).decode('utf-8')

    def checkPassword(self, psw):
        config = configparser.ConfigParser()
        config.read('data.env')
        envPsw = config['DEFAULT']['password']
        if psw == envPsw:
            return psw
        else:
            print("Password errata")
            sys.exit(0)
