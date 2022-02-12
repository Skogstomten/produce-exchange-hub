import base64

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def generate_salt() -> bytes:
    salt = get_random_bytes(256)
    return base64.urlsafe_b64encode(salt)


def hash_password(password: str, salt: bytes) -> str:
    hashed_value = PBKDF2(password, salt, 64, 1000000, hmac_hash_module=SHA512)
    hashed_value = base64.urlsafe_b64encode(hashed_value + salt)
    hashed_value = hashed_value.decode('utf-8')
    return hashed_value


def is_correct_password(in_password: str, hashed_password: str) -> bool:
    hashed_password_bytes = hashed_password.encode('utf-8')
    hashed_password_bytes = base64.urlsafe_b64decode(hashed_password_bytes)
    salt = hashed_password_bytes[64:]
    hashed_in_password = hash_password(in_password, salt)
    return hashed_in_password == hashed_password
