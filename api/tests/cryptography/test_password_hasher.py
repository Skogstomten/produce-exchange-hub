from sys import getsizeof
from base64 import urlsafe_b64decode

from unittest import TestCase

from app.cryptography.password_hasher import (
    generate_salt,
    is_correct_password,
    hash_password,
)


class PasswordHasherTest(TestCase):
    def test_generate_salt_generates_correct_length_salt(self):
        salt: bytes = generate_salt()
        salt = urlsafe_b64decode(salt)
        self.assertEqual(len(salt), 256)

    def test_hashing_works(self):
        clear_text_password: str = 'thisIsPassword'
        salt: bytes = generate_salt()
        hashed_password: str = hash_password(clear_text_password, salt)
        self.assertNotEqual(clear_text_password, hashed_password)

    def test_is_correct_password(self):
        clear_text_password: str = 'ThisIsPassword'
        salt: bytes = generate_salt()
        hashed_password: str = hash_password(clear_text_password, salt)
        self.assertTrue(is_correct_password(clear_text_password, hashed_password))
        self.assertFalse('wrongPassword', hashed_password)
