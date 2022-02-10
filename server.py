#pip3 install -U PyCryptodome 

import socket
import threading
import random
import string
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import pyperclip
import time
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

HOST = token=os.environ['HOST']
PORT = token=int(os.environ['PORT'])

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class oneClip(object):
    def __init__(self): 
        self.connected = 0
        self.t1 = threading.Thread(target=self.monitor_remote)
        self.t2 = threading.Thread(target=self.monitor_clipboard)
        self.connect()

    def isConnected(self):
        return self.connected

    def generate_key(self):
        size = 20
        chars = string.ascii_uppercase + string.digits
        self.psk = ''.join(random.choice(chars) for _ in range(size))
        self.cryptoCipher = AESCipher(self.psk)
    
    def threadsAlive(self):
        if (self.t1.is_alive() or self.t2.is_alive()):
            return True
        else:
            return False
    
    def connect(self):
        while (self.isConnected() == 0 and not self.threadsAlive()):
            try:
                print("Opening socket for connection. Client to connect to {}:{}".format(HOST, PORT))
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((HOST, PORT))
                self.s.listen(5)
                self.conn, self.addr = self.s.accept()
                self.conn.send("".encode())
                print("Connected to peer")
                self.generate_key()
                self.conn.send("oneclip://psk={}".format(self.psk).encode())
                print("Sent: oneclip://psk={}".format(self.psk))
                self.connected = 1
                try:
                    self.t1 = threading.Thread(target=self.monitor_remote)
                    self.t2 = threading.Thread(target=self.monitor_clipboard)
                    self.t1.start()
                    self.t2.start()
                except Exception as e:
                    print("Error: unable to start threads")
                    print(e)
                print('Threads started')
            except Exception as e: 
                print(e)

    def monitor_remote(self):
        while (self.isConnected() == 1):
            message = self.conn.recv(2048)
            # Check if message is blank. If it isn't proceed. If it is, close the socket (reset).
            if message:
                data = (self.cryptoCipher.decrypt(message)).strip('\n')
                self.previous = data
                print ("Recieved:", data)
                pyperclip.copy(data)
            else:
                self.conn.close()
                self.s.close()
                self.connected = 0
                print("Disconnected from peer")
                break

    def monitor_clipboard(self):
        self.previous = pyperclip.paste()

        while True:
            if (self.isConnected() == 1):
                self.current = pyperclip.paste()
                if (self.current != self.previous):
                    self.previous = self.current
                    print ("Sent:", self.current)
                    self.conn.send((self.cryptoCipher.encrypt(self.current)))
                # required to prevent reciever from sending the recieved clipboard back to the sender
                time.sleep(1)
            else:
                print("Disconnected from peer")
                break

object = oneClip()
while True:
    if (not object.threadsAlive()):
        del object
        object = oneClip()
