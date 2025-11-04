import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
DATABASE_PATH = os.getenv("DATABASE_PATH", "orders.db")
