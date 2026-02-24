import logging
from pathlib import Path

from src.app.core.config import SQLFileSettings, settings

BASE_FILE:str = settings.BASE_FILE if isinstance(settings,SQLFileSettings) else ""
LOGGER = logging.getLogger(__name__)

def read_sql_query(sql_path: str) -> str | None:
    """Read SQL file as string."""
    sql = Path(BASE_FILE + sql_path)
    if sql.exists():
        return sql.read_text()
    else:
        LOGGER.error("Files not found")
        return None

