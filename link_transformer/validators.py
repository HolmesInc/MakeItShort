from .models import URL


def validate_url_exists(url: str) -> bool:
    """
    Validate given domain is present in DB
    :param url: web site url
    :return True if domain is present False otherwise
    """
    return URL.objects.filter(origin_url=url).exists()
