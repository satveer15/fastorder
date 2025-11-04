from fastapi import FastAPI
from app.auth.router import router as auth_router

app = FastAPI(title="Order Management API")


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}


app.include_router(auth_router)
