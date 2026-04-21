"""Rate limiter — tek kaynak, circular import engelleme.

main.py ve tüm route modülleri buradan `limiter`'ı import eder.
Nginx proxy arkasında gerçek IP X-Forwarded-For header'ından alınır.
"""
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def real_client_ip(request: Request) -> str:
    """Nginx proxy arkasında gerçek kullanıcı IP'sini döndür."""
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=real_client_ip)
