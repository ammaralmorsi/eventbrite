from fastapi import FastAPI

from routers.categories import categories

app = FastAPI(
    title="EventBrite",
    description="EventBrite API",
    version="1.0",
)

app.include_router(categories.router)
