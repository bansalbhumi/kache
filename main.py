from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title='Kache',
    description='In-memory LRU Cache with TTL and REST API',
    version='1.0.0'
)

app.include_router(router, prefix='/cache')