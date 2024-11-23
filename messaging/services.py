import smtplib
from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from config import settings
from messaging.models import Attempt, Mailing


def check_and_send_mailings():
    current_time = timezone.now()

    mailings = Mailing.objects.filter(
        status=Mailing.Status.CREATED, periodicity__lte=current_time, is_active=True
    )

    for mailing in mailings:
        if can_send_mailing(mailing):
            send_mailing(mailing)


def can_send_mailing(mailing: Mailing) -> bool:
    last_attempt = (
        Attempt.objects.filter(
            mailing=mailing, status=Attempt.Status.SUCCESS
        )
        .order_by("-attempt_time")
        .first()
    )

    if not last_attempt:
        return True

    periodicity_map = {
        Mailing.Periodicity.DAILY: timedelta(days=1),
        Mailing.Periodicity.WEEKLY: timedelta(weeks=1),
        Mailing.Periodicity.MONTHLY: timedelta(days=30),
    }
    next_send_time = last_attempt.attempt_time + periodicity_map[mailing.periodicity]

    can_send = timezone.now() >= next_send_time
    return can_send


def send_mailing(mailing: Mailing):
    clients = mailing.clients.all()
    emails = [client.email for client in clients]

    attempt_status = Attempt.Status.SUCCESS
    server_response = None

    try:
        mailing.status = Mailing.Status.RUNNING
        mailing.save()

        send_mail(
            subject=mailing.message.title,
            message=mailing.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        mailing.status = Mailing.Status.CREATED

        if mailing.periodicity == Mailing.Periodicity.DAILY:
            mailing.at_start += timedelta(days=1)
        elif mailing.periodicity == Mailing.Periodicity.WEEKLY:
            mailing.at_start += timedelta(weeks=1)
        elif mailing.periodicity == Mailing.Periodicity.MONTHLY:
            mailing.at_start += timedelta(days=30)

        mailing.save()

    except smtplib.SMTPException as error:
        mailing.is_active = False
        mailing.save()
        attempt_status = Attempt.Status.FAILURE
        server_response = str(error)

    finally:
        Attempt.objects.create(
            mailing=mailing, status=attempt_status, server_response=server_response
        )
