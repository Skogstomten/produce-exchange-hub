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
    user_id = user_id.encode('utf-8')
    value = value.encode('utf-8')
    hasher = SHA512.new(user_id + value)
    hashed_value = hasher.digest()
    hashed_value = base64.urlsafe_b64encode(hashed_value + user_id)
    hashed_value = hashed_value.decode('utf-8')
    return hashed_value


def extract_user_id(key: str) -> str:
    hashed_value = key.encode('utf-8')
    hashed_value = base64.urlsafe_b64decode(hashed_value)
    user_id = hashed_value[64:]
    return str(user_id)


def key_is_valid(key: str, user_id: str, *args) -> bool:
    generated_key = generate_key_from_data(user_id, args)
    return generated_key == key
