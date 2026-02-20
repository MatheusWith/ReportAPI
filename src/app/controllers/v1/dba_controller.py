from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.dba_database import async_get_dba
from src.app.schema.vend_schema import PaginatedResponse, VendParams
from src.app.service import vend_service
from src.app.service.dependencies import read_sql_query

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
