# Architecture & Design Decisions

Notes on why I built things the way I did.

## Design Goals

Build something minimal but not toy-like. Show real-world patterns without over-engineering it.

Key ideas:
- Keep it simple
- Use standard tools everyone knows
- Don't skip security
- Code should be readable

## Key Decisions

### 1. Why FastAPI?

I went with FastAPI instead of Flask or Django because:

- Auto-generates API docs (saves a ton of time)
- Type hints everywhere makes it easier to catch bugs
- Pydantic validation built-in
- It's fast and has good docs
- Async support if we need it later

Downsides:
- It's newer than Flask (but production-ready now)
- Async might be overkill here but doesn't hurt

### 2. Why SQLite?

Could've used Postgres, but SQLite works great for this:

- Zero setup - just a file
- Easy to delete and start fresh during dev
- Perfect for demos and tests
- Switching to Postgres later is easy with SQLAlchemy

Downsides:
- Can't handle tons of concurrent writes (not an issue here)
- Missing some fancy Postgres features (don't need them)

Migration is literally one line:
```python
DATABASE_URL = "postgresql://user:pass@localhost/dbname"
```

### 3. APScheduler instead of Celery

For the background job, I used APScheduler because:

- No external dependencies (Redis, RabbitMQ, etc)
- Runs in the same process
- Perfect for simple interval jobs
- Much easier to debug

When would I use Celery instead?
- Need multiple workers
- Complex task routing
- Distributed execution
- Retry logic with backoff

For a job that runs every 2 minutes, APScheduler is plenty.

### 4. JWT Tokens (15 min expiry)

JWT made sense because:

- Stateless - no session storage needed
- Works everywhere (web, mobile, etc)
- Standard approach

Why 15 minutes? It's a tradeoff:
- Shorter = more secure if token leaks
- Longer = better UX (less re-login)

In a real app, I'd add refresh tokens:
- Access token: 15 min (short-lived)
- Refresh token: 7 days (long-lived)
- Auto-refresh without making user login again

### 5. bcrypt for passwords

Using bcrypt because:

- Intentionally slow (makes brute-forcing hard)
- Can increase cost factor over time
- Each password gets a unique salt
- Battle-tested since forever

Could've used Argon2 (newer, won a competition) but bcrypt is more common and just as secure for our needs.

### 6. SQLAlchemy ORM

Went with SQLAlchemy over raw SQL:

- Works with any DB (SQLite, Postgres, etc)
- Prevents SQL injection automatically
- Handles relationships nicely
- More Pythonic than writing SQL strings

Downsides:
- Slight learning curve
- Tiny performance hit (not noticeable here)

It's basically the standard ORM for Python at this point.

### 7. Order Status Flow

```
pending -> processing -> completed
   |
   └─> cancelled
```

Why this flow?

1. **pending** - Gives user time to cancel
2. **processing** - Shows it's being worked on, prevents cancellation
3. **completed** - Done
4. **cancelled** - User cancelled while pending

Simple rules:
- Can only cancel `pending` orders
- Once it hits `processing`, no going back
- Background job moves things along

### 8. Authorization

Keep it simple:
- Users see only their orders
- Users can only cancel their own orders
- Check on every request

```python
if order.user_id != current_user.id:
    raise HTTPException(403, "Not your order")
```

Didn't bother with roles (admin, manager, etc) since we don't need them. Can add later if needed.

## Security Notes

**Passwords:**
- Never stored plain
- Never returned in responses
- bcrypt hashed

**JWT:**
- 15 min expiry
- Secret in `.env` (never hardcode)
- Would use HTTPS in production

**SQL Injection:**
- SQLAlchemy handles it
- No raw SQL with user input

**Authorization:**
- JWT required for orders
- Ownership checked
- Proper 403/401 responses

## Database Indexes

Added indexes for common queries:

```sql
-- Fast login
CREATE INDEX idx_users_email ON users(email);

-- Fast user order lookups
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Fast background job queries
CREATE INDEX idx_orders_status ON orders(status);
```

SQLite is pretty fast even without these, but they help.

## Background Job

Chose 2 minutes as the interval:
- Immediate processing = no cancel ability
- Hours = bad UX
- 2 min = sweet spot

Job runs in a background thread via APScheduler. Each run is independent, so if one order fails it doesn't break others.

## Testing

Got tests for:
- User registration (including duplicate emails)
- Login (valid/invalid creds)
- Order creation
- Order listing (scoped to user)
- Order cancellation (pending only, ownership check)

Run with `pytest tests/ -v`

## What Would Change for Production?

**Database:**
Switch to PostgreSQL - just change the connection string.

**Background Jobs:**
Maybe move to Celery if we need multiple workers or complex task routing.

**Secrets:**
Use proper secrets manager (AWS Secrets, Vault) instead of `.env`

**HTTPS:**
Enforce it. Easy with nginx or middleware.

**Rate Limiting:**
Add `slowapi` or similar to prevent abuse.

**Monitoring:**
- Sentry for errors
- Prometheus + Grafana for metrics
- Structured JSON logs

**Scaling:**
- Postgres with connection pooling
- Multiple API instances behind nginx
- Redis for caching if needed

## Current Limitations

These are intentional for keeping it simple:

- SQLite (single writer)
- APScheduler (single instance, won't work with multiple API servers)
- No pagination (fine for small datasets)
- No refresh tokens (UX could be better)

## What Worked Well

- FastAPI's auto docs saved time
- Pydantic validation eliminated a lot of manual checking
- SQLAlchemy made DB work cleaner
- Type hints caught bugs early
- APScheduler was perfect for simple scheduling

## Takeaways

- Match tools to problem size (don't over-engineer)
- Security matters even in demos
- Build for change (easy to swap SQLite for Postgres later)
- Start simple, add complexity when needed
- Comments and docs are worth it
