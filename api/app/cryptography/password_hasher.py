import base64

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def generate_salt() -> bytes:
    salt = get_random_bytes(256)
    return base64.urlsafe_b64encode(salt)


def hash_password(password: str, salt: str) -> str:
    hash = PBKDF2()
