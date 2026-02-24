from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.dba_database import async_get_dba
from src.app.core.setup import limiter
from src.app.schema.vend_schema import PaginatedResponse, VendParams
from src.app.service import vend_service

controller = APIRouter(tags=["dba"])

@controller.get("/dba/vend/",status_code=200,response_model=PaginatedResponse)
async def dba_vend(
    *,
    request:Request,
    db: Annotated[AsyncSession,Depends(async_get_dba)],
    params: Annotated[VendParams,Depends()],
) -> PaginatedResponse:

    return await vend_service.dba_vend_service(
        db=db,
        params=params,
    )
