from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.auth.router import router as auth_router
from app.orders.router import router as orders_router
from app.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(title="Order Management API", lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}


app.include_router(auth_router)
app.include_router(orders_router)
