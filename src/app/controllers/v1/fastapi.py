from fastapi import APIRouter

controller = APIRouter(tags=["fastapi"])

@controller.get("fasapi/")
def read_root():
    return {"Hello": "World"}


@controller.get("items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
