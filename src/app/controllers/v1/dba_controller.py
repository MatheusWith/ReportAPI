from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request


controller = APIRouter(tags=["dba"])

@controller.get("dba/vend/")
async def dba_vend(
    *,
    request:Request,
    params: Any
)