from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from routers.categories import categories
from routers.auth import auth
from routers.events import events


app = FastAPI(
    title="EventBrite",
    description="EventBrite API",
    version="1.0",
    docs_url="/"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(events.router)


add_pagination(app)
