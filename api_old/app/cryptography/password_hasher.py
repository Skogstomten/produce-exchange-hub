import base64

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def generate_salt() -> bytes:
    salt = get_random_bytes(256)
    return base64.urlsafe_b64encode(salt)


def hash_password(password: str, salt: bytes) -> str:
    hash = PBKDF2(password.encode('utf-8'), salt, 64, 1000000, hmac_hash_module=SHA512)
    hash = base64.urlsafe_b64encode(hash + salt)
    hash = hash.decode('utf-8')
    return hash


def is_correct_password(in_password: str, hashed_password: str) -> bool:
    hashed_password_bytes = hashed_password.encode('utf-8')
    hashed_password_bytes = base64.urlsafe_b64decode(hashed_password_bytes)
    salt = hashed_password_bytes[64:]
    hashed_in_password = hash_password(in_password, salt)
    return hashed_in_password == hashed_password
