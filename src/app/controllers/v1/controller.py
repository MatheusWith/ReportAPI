from fastapi import APIRouter

from src.app.controllers.v1.fastapi import controller as controller_fastapi

controller = APIRouter(prefix="/v1")
controller.include_router(controller_fastapi)