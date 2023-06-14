# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:25:57 2023

@author: wingh
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
"""key = Fernet.generate_key()
f = Fernet(key)
with open('key.key',"wb") as file:
    file.write(key)    
"""
"""
with open('key.key',"rb") as file:
    key = file.read()
password = b"password"
salt = os.urandom(16)
print(salt)
with open('salt.salt',"wb") as file:
    file.write(salt) 
"""

class InvalidSignature(Exception):
    pass
class InvalidToken(Exception):
    pass
#password = "password"
password = input("Please enter the password:\n")
password = password.encode()
with open('salt.salt',"rb") as file:
    salt = file.read()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
realkey = base64.urlsafe_b64encode(kdf.derive(b"password"))
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
def add():
    with open('pw.txt',"a") as file:
        title = input("Enter the title:\n")
        pw = input("Enter the password of this title:\n")
        EncryptedTitle = f.encrypt(title.encode())
        EncryptedPw = f.encrypt(pw.encode())    
        #print(f.decrypt(EncryptedTitle))
        try:
            file.write(EncryptedTitle.decode() + "\n") 
            file.write(EncryptedPw.decode()+"\n")
        except:
            print("seems like there is an error,please input again")
        else:
            print("Save successful")
    

def view():
    with open('pw.txt',"r") as file:
        try:
            for line in file:            
                print(f.decrypt(line.rstrip()).decode())
                print("\n")
        except:
            print("Error, fail to view the content")
def delete():
    delData = input("which title you want to delete:\n")
    lock = 0
    datas = list()
    deleted = 0
    with open('pw.txt',"r") as file:
        datas = file.readlines()
    #print(datas)
    #for data in datas:
        #print(f.decrypt(data.encode()).decode())
    
    with open('pw.txt',"w") as file:           
        for data in datas:
            if(f.decrypt(data.encode()).decode() == delData):
                lock = 1
                deleted = 1
            else:
                if(lock == 0):
                    file.write(data) 
                if(lock == 1):
                    lock = 0
            #print(f.decrypt(data.rstrip()).decode())
    if(deleted):
        print("Data deleted")
    else:
        print("No such item in the file")
    
    
    """   
        data.append(f.decrypt(line.rstrip()).decode())
        if(data == delData):
            lock = 1
        else:
            if(lock == 0):
                with open('pw.txt',"w") as file2:
                    file2.write(f.encrypt(data.encode()).decode() + "\n") 
            if(lock == 1):
                lock = 0
    """
        
          
while True:
    if(key != realkey):
        print("seems like you enter a wrong password,try again next time ;)")
        break
    choice = input("Which operation you want to do:add,view,delete or exit\n")
    
    match choice:
        case "add":
            add()
        case "view":
            view()
        case "delete":
            delete()
        case "exit":
            break
        case default:
            print("Invalid operation please input again")

    