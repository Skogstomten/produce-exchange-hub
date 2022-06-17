"""
Contains methods for hashing, verifying and generating salt for passwords
"""
import base64

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def generate_salt() -> bytes:
    """
    Generates a random 256 byte long salt

    >>> s = generate_salt()
    >>> len(s)
    256

    :return: bytes 256 long, urlsafe b64 encoded
    """
    return get_random_bytes(256)


def hash_password(password: str, salt: bytes) -> str:
    """
    Hashes a password using PBKDF2 algorith

    >>> s = b'salt'
    >>> hash_password('Password', s)
    '1OBCLoBuoHI9JCC662fmmxiLAXsOz8xbrBlsQzQ92TIWesr8knPRbL4waA0RKMABsurKCFdJrE3BI-cnAoo3sHNhbHQ='

    :param password: password to be hashed
    :param salt: salt to use
    :return: hashed password with salt as base64 encoded byte string
    """
    hashed_bytes = PBKDF2(password, salt, 64, 1000000, hmac_hash_module=SHA512)
    hashed_bytes = base64.urlsafe_b64encode(hashed_bytes + salt)
    hashed_value = hashed_bytes.decode("utf-8")
    return hashed_value


def is_correct_password(in_password: str, hashed_password: str) -> bool:
    """
    Verifies that provided password is same as hashed password

    >>> hashed = '1OBCLoBuoHI9JCC662fmmxiLAXsOz8xbrBlsQzQ92TIWesr'
    ...          '8knPRbL4waA0RKMABsurKCFdJrE3BI-cnAoo3sHNhbHQ='
    >>> is_correct_password('Password', hashed)
    True

    >>> hashed = '1OBCLoBuoHI9JCC662fmmxiLAXsOz8xbrBlsQzQ92TIWes'
    ...          '8knPRbL4waA0RKMABsurKCFdJrE3BI-cnAoo3sHNhbHQ='
    >>> is_correct_password('WrongPassword', hashed)
    False

    :param in_password:
    :param hashed_password:
    :return: True of password is a match
    """
    hashed_password_bytes = hashed_password.encode("utf-8")
    hashed_password_bytes = base64.urlsafe_b64decode(hashed_password_bytes)
    salt = hashed_password_bytes[64:]
    hashed_in_password = hash_password(in_password, salt)
    return hashed_in_password == hashed_password
