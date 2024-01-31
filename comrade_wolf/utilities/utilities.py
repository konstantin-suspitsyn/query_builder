import string
import random


def generate_random_string(length: int) -> str:
    """
    Generate randow string
    :param length: string length
    :return: random string
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
