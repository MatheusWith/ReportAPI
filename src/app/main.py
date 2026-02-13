from src.app.controllers.controller import controller
from src.app.core.config import settings
from src.app.core.setup import create_application, lifespan_factory

lifespan = lifespan_factory(settings=settings)

app = create_application(
    router=controller,
    settings=settings,
    lifespan=lifespan
)


