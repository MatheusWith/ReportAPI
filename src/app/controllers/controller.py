from fastapi import APIRouter

from src.app.controllers.v1.controller import controller as controller_fastapi

controller = APIRouter(prefix="/api")

controller.include_router(controller_fastapi)