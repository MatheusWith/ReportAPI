from slowapi import Limiter
from slowapi.util import get_remote_address

from src.app.core.config import SlowapiSettings, settings

GLOBAL_GENERIC_LIMIT:int = settings.GLOBAL_GENERIC_LIMIT if isinstance(settings, SlowapiSettings) else 60

limiter = Limiter(key_func=get_remote_address,  default_limits=["60/minute"])
