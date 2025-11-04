from fastapi import FastAPI

app = FastAPI(title="Order Management API")


@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}
