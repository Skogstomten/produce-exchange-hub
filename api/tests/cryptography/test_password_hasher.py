from base64 import urlsafe_b64decode

from app.cryptography.password_hasher import (
    generate_salt,
    is_correct_password,
    hash_password,
)


def test_generate_salt_generates_correct_length_salt():
    salt: bytes = generate_salt()
    salt = urlsafe_b64decode(salt)
    assert len(salt) == 256


def test_hashing_works():
    clear_text_password: str = 'thisIsPassword'
    salt: bytes = generate_salt()
    hashed_password: str = hash_password(clear_text_password, salt)
    assert clear_text_password != hashed_password


def test_is_correct_password():
    clear_text_password: str = 'ThisIsPassword'
    salt: bytes = generate_salt()
    hashed_password: str = hash_password(clear_text_password, salt)
    assert is_correct_password(clear_text_password, hashed_password)
    assert not is_correct_password('wrong_password', hashed_password)
