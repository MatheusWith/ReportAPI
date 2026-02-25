import logging
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schema.vend_schema import PaginatedResponse, Vend, VendAllQuantityParams, VendPaginationParams
from src.app.service.dependencies import read_sql_query

LOGGER = logging.getLogger(__name__)

async def dba_vend_service(
    *,
    db:AsyncSession,
    params: VendPaginationParams,
) -> PaginatedResponse[Vend]:
    sql:str = read_sql_query("vend/vend.sql")
    sql_count:str = read_sql_query("vend/vend_count.sql")

    if sql is None or sql_count is None:
        raise HTTPException(status_code=500, detail="Internal server configuration error")

    qp_count: dict[str, date | int | str] = {
        "start_date": params.start_date,
        "end_date": params.end_date,
    }
    qp_query:dict[str, date | int | str] = qp_count.copy()
    qp_query["limit"] = params.per_page
    qp_query["offset"] = params.offset

    try:
        result_query = await db.execute(
            text(sql),
            qp_query,
        )

        result_count = await db.execute(
            text(sql_count),
            qp_count,
        )
    except SQLAlchemyError:
        LOGGER.error("It doesn't connect to the database.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="It doesn't connect to the database."
        )

    datas:list[Vend] = [Vend(**rq) for rq in result_query.mappings().all()]
    count: int = result_count.scalar_one()
    current_page:int = params.current_page
    total_pages:int = (count + params.per_page - 1) // params.per_page


    return PaginatedResponse[Vend](
        datas=datas,
        count=count,
        current_page=current_page,
        total_pages=total_pages,
        per_page=params.per_page,
    )

async def dba_vend_report_service(
    *,
    db:AsyncSession,
    params:VendAllQuantityParams,
) -> list[Vend]:
    sql:str = read_sql_query("vend/vend_report.sql")
    sql_count:str = read_sql_query("vend/vend_count.sql")
    if sql is None or sql_count is None:
        raise HTTPException(status_code=500, detail="Internal server configuration error")

    try:
        qp_count: dict[str, date | int | str] = {
            "start_date": params.start_date,
            "end_date": params.end_date,
        }

        result_count = await db.execute(
            text(sql_count),
            qp_count,
        )
        count:int = result_count.scalar_one()

        qp_query:dict[str, date | int | str] = qp_count.copy()

        qp_query["limit"] = count if params.all_items else params.quantity

        query = await db.execute(
            text(sql),
            qp_query,
        )

    except SQLAlchemyError:
        LOGGER.error("It doesn't connect to the database.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="It doesn't connect to the database."
        )

    datas:list[Vend] = [Vend(**q) for q in query.mappings().all()]
    return datas
