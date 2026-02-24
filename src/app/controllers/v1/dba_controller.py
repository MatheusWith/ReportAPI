from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.dba_database import async_get_dba
from src.app.schema.vend_schema import PaginatedResponse, Vend, VendAllQuantityParams, VendPaginationParams
from src.app.service import vend_service

controller = APIRouter(tags=["dba"])

@controller.get("/dba/vend/",status_code=200,response_model=PaginatedResponse[Vend])
async def dba_vend(
    *,
    request:Request,
    db: Annotated[AsyncSession,Depends(async_get_dba)],
    params: Annotated[VendPaginationParams,Depends()],
) -> PaginatedResponse[Vend]:

    return await vend_service.dba_vend_service(
        db=db,
        params=params,
    )

@controller.get("/dba/vend/report/", status_code=200, response_model=list[Vend])
async def dba_vend_report(
    *,
    request:Request,
    db: Annotated[AsyncSession,Depends(async_get_dba)],
    params: Annotated[VendAllQuantityParams,Depends()],
) -> list[Vend]:
    return await vend_service.dba_vend_report_service(
        db=db,
        params=params
    )
