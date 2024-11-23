from apscheduler.schedulers.background import BackgroundScheduler

from messaging.services import check_and_send_mailings


# Запуск планировщика
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_mailings, "interval", seconds=10)
    scheduler.start()

