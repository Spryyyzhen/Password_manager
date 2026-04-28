from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


file_src = Path(__file__).resolve().parent


def generate_key(password=str, salt=bytes) -> bytes:
    """
    Generates a random SHA256 key in order to encrypt a wallet.
    """

    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000)

    return base64.urlsafe_b64encode(key.derive(password.encode()))


def encrypt_wallet(name=str, password=str) -> None:
    """
    Function that encrypts the user's .json wallet and will transform it into a .enc file.\n
    Takes both the user's name and his password.
    """

    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    file = file_src.parent / "wallets" / f"{name}_wallet.json"
    with open(file, "rb") as f:
        data = f.read()
    
    os.remove(file)

    encrypted_data = fernet.encrypt(data)

    with open(file_src.parent / "wallets" / f"{name}_wallet.enc", "wb") as f:
        f.write(salt + encrypted_data)


def decrypt_wallet(name=str, password=str) -> int:
    """
    Function that decrypts the user's .enc wallet and transforms it into a .json file.\n
    Takes both the user's name and his password.\n
    Returns 0 if the file is successfully decrypted, returns -1 if the password is incorrect and returns -2 if the wallet doesn't exist.
    """

    try:

        file = file_src.parent / "wallets" / f"{name}_wallet.enc"
        
        with open(file, "rb") as f:
            data = f.read()
        
        os.remove(file)

        salt = data[:16]
        encrypted_data = data[16:]

        key = generate_key(password, salt)
        fernet = Fernet(key)

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_src.parent / "wallets" / f"{name}_wallet.json", "wb") as f:
            f.write(decrypted_data)
        
        return 0
    
    except FileNotFoundError:
        return -2
    
    except Exception:
        return -1


def create_wallet(name=str, password=str) -> int:
    """
    The function that allows the creation of a wallet (in other words, the creation of a password manager user) and encrypt this wallet.\n
    Returns 0 if a wallet has been created, returns -1 if a wallet with this name already exists.
    """

    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    if file.exists():
        return -1
    else:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(f'{{\n\t"Wallet of {name}" : []\n}}')
        
        encrypt_wallet(name, password)
        return 0