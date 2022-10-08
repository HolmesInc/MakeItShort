import hashlib
from typing import Union


def collect_user_data(meta: dict) -> Union[str, None]:
    """
    Extract user data from incoming request metadata
    :param meta: request metadata
    :return User IP address
    """
    forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        user_ip = forwarded_for.split(',')[0]
    else:
        user_ip = meta.get('REMOTE_ADDR')
    return user_ip
