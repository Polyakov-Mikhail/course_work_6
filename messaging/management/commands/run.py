from django.core.management import BaseCommand
from apscheduler.schedulers.background import BlockingScheduler
from messaging.services import is_started, daily, weekly, monthly


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        scheduler = BlockingScheduler()
        scheduler.add_job(is_started, 'interval', day=1)
        scheduler.add_job(daily, 'interval', day=1)
        scheduler.add_job(weekly, 'interval', week=1)
        scheduler.add_job(monthly, 'interval', month=1)
        scheduler.start()
