import logging
from pathlib import Path

from src.app.core.config import settings

base_file:str = settings.BASE_FILE

LOGGER = logging.getLogger(__name__)

def read_sql_query(sql_path: str) -> str | None:
    """Read SQL file as string."""
    sql = Path(base_file + sql_path)
    if sql.exists():
        return sql.read_text()
    else:
        LOGGER.error("Files not found")
        return None

