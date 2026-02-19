from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schema.vend_schema import VendParams


controller = APIRouter(tags=["dba"])

@controller.get("dba/vend/")
async def dba_vend(
    *,
    request:Request,
    params: Annotated[VendParams,Depends()],
    dba: Annotated[Asyn]
)