from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.dba_database import async_get_dba
from src.app.schema.vend_schema import PaginatedResponse, VendParams, VendReport
from src.app.service.dependencies import read_sql_query


async def dba_vend_service(
    *,
    db: Annotated[AsyncSession,Depends(async_get_dba)],
    params: VendParams,
) -> PaginatedResponse:
    try:
        sql = read_sql_query("src/app/sql/vend.sql")
        sql_count = read_sql_query("src/app/sql/vend_count.sql")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="internal server configuration error")

    try:
        query = await db.execute(
            text(sql),
            {
                "start_date": params.start_date,
                "end_date": params.end_date,
                "limit": params.per_page,
                "offset": params.offset,
            },
        )

        count = await db.execute(
            text(sql_count),
            {
                "start_date": params.start_date,
                "end_date": params.end_date,
            }
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="it doesn't connect to the database."
        )

    return PaginatedResponse(
        datas=[VendReport(**row) for row in query.mappings().all()],
        count=count.scalar_one(),
        current_page=params.current_page,
        total_pages=(count + params.per_page - 1) // params.per_page,
    )