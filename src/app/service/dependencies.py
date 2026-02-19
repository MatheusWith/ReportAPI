from pathlib import Path


def read_sql_query(sql_path: str) -> str:
    """Read SQL file as string."""
    return Path(sql_path).read_text()
