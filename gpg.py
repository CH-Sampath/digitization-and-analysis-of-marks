import os
import tarfile
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from getpass import getpass
import base64
from remove_cache import rmcache

def compress_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    tar_file = f"{folder_name}.tar"
    with tarfile.open(tar_file, "w:gz") as tar:
        tar.add(folder_path, arcname=folder_name)
    return tar_file

def decompress_folder(tar_file, output_folder):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall(path=output_folder)

def remove_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def remove_folder(folder_path):
    shutil.rmtree(folder_path)

def get_key(password_provided):
    password = password_provided.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_file(file_name, key):
    fernet = Fernet(key)
    with open(file_name, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_name, key):
    fernet = Fernet(key)
    with open(file_name, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_name, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

def gpg(operation, path):

    # operation = input("Enter 'c' for compression or 'd' for decompression: ")
    # path = input("Enter folder path (for compression) or tarball file path (for decompression): ")
    passphrase = getpass("Enter passphrase: ")

    if operation == 'c':
        tar_file = compress_folder(path)
        encrypt_file(tar_file, get_key(passphrase))
        remove_folder(path)
    elif operation == 'd':
        decrypt_file(path, get_key(passphrase))
        decompress_folder(path, os.path.dirname(path))
        remove_files(path)
    else:
        print("Invalid operation choice.")

if __name__ == "__main__":
    rmcache("C:\\major-version1.0\\resizedto1400")
    if os.path.isfile("C:\\major-version1.0\\keys.tar") and os.path.isfile("C:\\major-version1.0\\Excels.tar"):
        operation = 'd'
        gpg(operation, "C:\\major-version1.0\\keys.tar")
        gpg(operation, "C:\\major-version1.0\\Excels.tar")
    else:
        operation = 'c'
        gpg(operation, "C:\\major-version1.0\\keys")
        gpg(operation, "C:\\major-version1.0\\Excels")

# gpg('c', 'C:\\major-version1.0\\keys')
# gpg('c', 'C:\\major-version1.0\\Excels')