"""Entry point for running the FastAPI application"""
import uvicorn
from app.database import init_db

if __name__ == "__main__":
    # Initialize database tables
    init_db()

    # Start the server - scheduler will auto-start via lifespan
    # Tested: background jobs are working! Orders move from pending -> processing -> completed
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
