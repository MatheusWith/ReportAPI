from src.app.core.config import settings
from src.app.core.setup import create_application, lifespan_factory

lifespan = lifespan_factory(settings=settings)

app = create_application(
    # router=router,
    settings=settings,
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
