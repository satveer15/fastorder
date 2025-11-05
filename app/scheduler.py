from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()


def start_scheduler():
    """Initialize and start the background scheduler"""
    if not scheduler.running:
        scheduler.start()
        print("Background scheduler started")


def stop_scheduler():
    """Shutdown the scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        print("Background scheduler stopped")
