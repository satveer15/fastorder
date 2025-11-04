# Order Management API

A FastAPI-based order management system with JWT auth, SQLite, and background processing.

## Features

- JWT authentication (15 min token expiry)
- Order CRUD operations (create, list, cancel)
- Background job that processes orders every 2 minutes
- bcrypt password hashing
- Pydantic validation
- Auto-generated API docs at `/docs`

## Tech Stack

- FastAPI 0.104.1
- SQLite + SQLAlchemy 2.0
- JWT auth (python-jose + passlib/bcrypt)
- APScheduler for background jobs
- Pydantic for validation
- pytest for testing

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env and change JWT_SECRET to something random
```

### 3. Run it

```bash
python run.py
```

Server starts at **http://localhost:8000**

- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/

## API Endpoints

**Auth:**
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

**Orders (requires auth):**
- `POST /orders` - Create new order
- `GET /orders` - List your orders
- `PATCH /orders/{id}/cancel` - Cancel a pending order

## Quick Test with curl

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"secure123"}'

# Login (save the token)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"secure123"}'

# Create order (use your token)
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"product_name":"Laptop","amount":999.99}'

# List orders
curl http://localhost:8000/orders \
  -H "Authorization: Bearer YOUR_TOKEN"

# Cancel order
curl -X PATCH http://localhost:8000/orders/1/cancel \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Or just use the interactive docs at http://localhost:8000/docs

## Running Tests

```bash
pytest tests/ -v
```

## Order Status Flow

```
pending -> processing -> completed
   |
   └─> cancelled (user action)
```

Orders start as `pending`. Every 2 minutes, a background job picks them up and processes them to `completed`. Users can only cancel orders while they're still `pending`.

## Security

- Passwords hashed with bcrypt (never stored plain)
- JWT tokens expire after 15 minutes
- Users can only see/cancel their own orders
- Pydantic validates all inputs
- SQLAlchemy prevents SQL injection

## Background Job

APScheduler runs every 2 minutes to process pending orders:
1. Find all `pending` orders
2. Move to `processing`
3. Simulate work (0.5s delay)
4. Mark as `completed`

Check `api.log` for processing logs.

## Project Structure

```
app/
  ├── main.py              # FastAPI app + scheduler setup
  ├── config.py            # Environment config
  ├── database.py          # SQLAlchemy setup
  ├── models.py            # DB models (User, Order)
  ├── schemas.py           # Pydantic request/response schemas
  ├── auth/
  │   ├── router.py        # /auth/register, /auth/login
  │   ├── dependencies.py  # JWT token validation
  │   └── utils.py         # Password hashing, token creation
  ├── orders/
  │   └── router.py        # Order CRUD endpoints
  └── jobs/
      └── order_processor.py  # Background job logic
tests/
  ├── test_auth.py
  └── test_orders.py
migrations/
  └── init.sql             # DB schema
run.py                     # Entry point
```

## Common Issues

**"Could not validate credentials"** - Token expired (15 min limit). Login again.

**"Email already registered"** - Use a different email or just login.

**Database errors** - Try deleting `orders.db` and restarting.

## Environment Variables

```env
JWT_SECRET=change-this-to-something-random
JWT_ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=15
DATABASE_PATH=orders.db
HOST=0.0.0.0
PORT=8000
```

## TODO

- Add refresh tokens
- Rate limiting
- Pagination
- Switch to PostgreSQL for prod
- Docker setup

## Notes

See `ARCHITECTURE.md` for design decisions and reasoning.
