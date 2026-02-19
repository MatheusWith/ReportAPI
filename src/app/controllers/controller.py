from fastapi import APIRouter

from src.app.controllers.v1.controller import controller as controller_v1

controller = APIRouter(prefix="/api")

controller.include_router(controller_v1)