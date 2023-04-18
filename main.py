from fastapi import FastAPI

from routers.events import events
from routers.categories import categories
from routers.tickets import tickets
from routers.promocodes import promocodes

app = FastAPI(
    title="EventBrite",
    description="EventBrite API",
    version="1.0",
)

app.include_router(categories.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(promocodes.router)
