import string
from django.utils.crypto import get_random_string


def make_hash():
    """
    generates "random" 7 chars string contains lower/upper characters and numbers
    params size and chars are hardcoded, due to project requirements (hash length is 7 chars, contains upper/lower chars and numbers)
    """
    size = 7
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return get_random_string(size, chars)