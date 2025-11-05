from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from app.auth.router import router as auth_router
from app.orders.router import router as orders_router
from app.scheduler import start_scheduler, stop_scheduler
from app.exceptions import (
    sqlalchemy_exception_handler,
    jwt_exception_handler,
    general_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(title="Order Management API", lifespan=lifespan)

# Register exception handlers
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}


app.include_router(auth_router)
app.include_router(orders_router)
