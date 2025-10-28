import hashlib
import string


BASE62_ALPHABET = string.ascii_letters + string.digits


def _base62_encode(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()
    return "".join(arr)


def generate_short_url(original_url: str, salt: str, length: int = 8) -> str:
    hash_code = hashlib.sha256()
    hash_code.update(f"{salt}:{original_url}".encode("utf-8"))
    digest_int = int(hash_code.hexdigest(), 16)
    encoded = _base62_encode(digest_int)
    return encoded[:length]
