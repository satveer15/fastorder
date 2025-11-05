from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Order


def process_pending_orders():
    """
    Background job to process pending orders
    Simulates order processing by moving pending orders to processing status
    """
    db: Session = SessionLocal()
    try:
        # Find orders that are pending for more than 1 minute
        cutoff_time = datetime.utcnow() - timedelta(minutes=1)

        pending_orders = db.query(Order).filter(
            Order.status == "pending",
            Order.created_at <= cutoff_time
        ).all()

        processed_count = 0
        for order in pending_orders:
            order.status = "processing"
            processed_count += 1

        if processed_count > 0:
            db.commit()
            print(f"Processed {processed_count} pending orders at {datetime.utcnow()}")

    except Exception as e:
        print(f"Error processing orders: {e}")
        db.rollback()
    finally:
        db.close()


def complete_processing_orders():
    """
    Move processing orders to completed status
    Simulates completion after processing
    """
    db: Session = SessionLocal()
    try:
        # Orders that have been processing for more than 2 minutes
        cutoff_time = datetime.utcnow() - timedelta(minutes=2)

        processing_orders = db.query(Order).filter(
            Order.status == "processing",
            Order.updated_at <= cutoff_time
        ).all()

        completed_count = 0
        for order in processing_orders:
            order.status = "completed"
            completed_count += 1

        if completed_count > 0:
            db.commit()
            print(f"Completed {completed_count} processing orders at {datetime.utcnow()}")

    except Exception as e:
        print(f"Error completing orders: {e}")
        db.rollback()
    finally:
        db.close()
