import base64

from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def generate_key_from_data(user_id: str, *args) -> str:
    value = ''
    for val in args:
        if isinstance(val, str):
            value += val
        else:
            value += str(val)
    value = value.encode('utf-8')
    hasher = SHA512.new(user_id + value)
    hash = hasher.digest()
    hash = base64.urlsafe_b64encode(hash + user_id)
    hash = hash.decode('utf-8')
    return hash

def extract_user_id(key: str) -> str:
    hash = key.encode('utf-8')
    hash = base64.urlsafe_b64decode(hash)
    user_id = hash[64:]
    return user_id

def key_is_valid(key: str, user_id: str, *args) -> bool:
    generated_key = generate_key_from_data(user_id, args)
    return generated_key == key
