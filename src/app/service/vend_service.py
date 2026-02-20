import logging
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schema.vend_schema import PaginatedResponse, VendParams, VendReport
from src.app.service.dependencies import read_sql_query

LOGGER = logging.getLogger(__name__)

async def dba_vend_service(
    *,
    db:AsyncSession,
    params: VendParams,
) -> PaginatedResponse:
    sql:str = read_sql_query("vend.sql")
    sql_count:str = read_sql_query("vend_count.sql")

    if sql is None or sql_count is None:
        raise HTTPException(status_code=500, detail="Internal server configuration error")

    try:
        result_query = await db.execute(
            text(sql),
            {
                "start_date": params.start_date,
                "end_date": params.end_date,
                "limit": params.per_page,
                "offset": params.offset,
            },
        )

        result_count = await db.execute(
            text(sql_count),
            {
                "start_date": params.start_date,
                "end_date": params.end_date,
            }
        )
    except SQLAlchemyError as e:
        LOGGER.error("It doesn't connect to the database.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="It doesn't connect to the database."
        )

    datas = [VendReport(**rq) for rq in result_query.mappings().all()]
    count: int = result_count.scalar_one()
    current_page:int = params.current_page
    total_pages:int = (count + params.per_page - 1) // params.per_page


    return PaginatedResponse(
        datas=datas,
        count=count,
        current_page=current_page,
        total_pages=total_pages,
        per_page=params.per_page,
    )
