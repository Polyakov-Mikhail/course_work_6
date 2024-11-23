from time import sleep
from django.apps import AppConfig
import os
import sys


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"
    verbose_name = "Рассылки"

    # def ready(self):
    #     import messaging.receivers
    #     from messaging.scheduler import start_scheduler
    #     sleep(1)
    #     start_scheduler()

    def ready(self):
        if "runserver" in sys.argv and os.environ.get("RUN_MAIN") == "true":
            from messaging.scheduler import start_scheduler

            start_scheduler()
