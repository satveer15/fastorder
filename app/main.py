from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.orders.router import router as orders_router

app = FastAPI(title="Order Management API")


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}


app.include_router(auth_router)
app.include_router(orders_router)
