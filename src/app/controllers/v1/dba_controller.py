from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.app.schema.vend_schema import PaginatedResponse, VendParams
from src.app.service import vend_service

controller = APIRouter(tags=["dba"])

@controller.get("dba/vend/")
async def dba_vend(
    *,
    request:Request,
    params: Annotated[VendParams,Depends()],
) -> PaginatedResponse | HTTPException | Any:

    return await vend_service.dba_vend_service(params=params)
