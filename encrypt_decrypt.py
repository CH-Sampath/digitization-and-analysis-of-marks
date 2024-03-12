from cryptography.fernet import Fernet
import pandas as pd
import os

def save_key(key, file_path):
    with open(file_path, 'wb') as key_file:
        key_file.write(key)


def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        return key_file.read()




def encrypt_excel(name, sem, acyear, file_path):
    key_file_path = f'C:\\major-version1.0\\keys\\{str(name)}-{str(sem)}-{str(acyear)}.key'
    if os.path.exists(key_file_path):
        key = load_key(key_file_path)
    else:
        key = Fernet.generate_key()
        save_key(key, key_file_path)

    cipher_suite = Fernet(key)
    df = pd.read_excel(file_path)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: cipher_suite.encrypt(str(float(x)).encode()).decode() if pd.notnull(x) else x)
    df.to_excel(file_path, index=False)

def decrypt_excel(name, sem, acyear, file_path):
    key = load_key(f'C:\\major-version1.0\\keys\\{name}-{sem}-{acyear}.key')
    cipher_suite = Fernet(key)
    df = pd.read_excel(file_path)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: float(cipher_suite.decrypt(str(x).encode()).decode()) if pd.notnull(x) else x)
    df.to_excel(file_path, index=False)


# encrypt_excel("final", 6, 2023, "C:\\major-version1.0\\Excels\\final-6-2023.xlsx")
# decrypt_excel("final", 6, 2023, "C:\\major-version1.0\\Excels\\final-6-2023.xlsx")
