from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.jobs.order_processor import process_pending_orders, complete_processing_orders

scheduler = BackgroundScheduler()


def start_scheduler():
    """Initialize and start the background scheduler"""
    if not scheduler.running:
        # Run order processor every 30 seconds
        scheduler.add_job(
            process_pending_orders,
            trigger=IntervalTrigger(seconds=30),
            id="process_pending_orders",
            replace_existing=True
        )

        # Run completion job every 45 seconds
        scheduler.add_job(
            complete_processing_orders,
            trigger=IntervalTrigger(seconds=45),
            id="complete_processing_orders",
            replace_existing=True
        )

        scheduler.start()
        print("Background scheduler started with order processing jobs")


def stop_scheduler():
    """Shutdown the scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        print("Background scheduler stopped")
