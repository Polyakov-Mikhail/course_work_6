# Generated by Django 5.1.2 on 2024-11-04 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Электронная почта"
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Contacts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=50, verbose_name="Страна")),
                ("identity_nalog_number", models.IntegerField(verbose_name="ИНН")),
                ("address", models.TextField(verbose_name="Адрес")),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="URL"
                    ),
                ),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="Тема сообщения"),
                ),
                ("message", models.TextField(verbose_name="Сообщение")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="message/preview",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "permissions": [
                    ("cannot_change_message", "Не может изменять сообщения")
                ],
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time_sending",
                    models.DateTimeField(verbose_name="дата и время отправки"),
                ),
                (
                    "time_end",
                    models.DateTimeField(verbose_name="дата и время окончания"),
                ),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("once a week", "один раз в неделю"),
                            ("everyday", "каждый день"),
                            ("once a month", "один раз в месяц"),
                        ],
                        max_length=100,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "создана"),
                            ("launched", "запущена"),
                            ("completed", "завершена"),
                        ],
                        max_length=100,
                        verbose_name="статус",
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        to="messaging.client", verbose_name="клиенты"
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="messaging.message",
                        verbose_name="сообщение",
                    ),
                ),
            ],
            options={
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
                "permissions": [
                    ("can_view_mailing", "Может просматривать рассылки"),
                    ("can_disable_mailing", "Может отключать рассылки"),
                    ("cannot_edit_mailing", "Не может редактировать рассылки"),
                    ("cannot_manage_mailing", "Не может управлять списком рассылок"),
                    ("cannot_change_mailing", "Не может создавать рассылки"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Attempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time_attempt",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время попытки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("successful", "успешно"),
                            ("unsuccessful", "не успешно"),
                        ],
                        max_length=100,
                        verbose_name="статус попытки",
                    ),
                ),
                (
                    "answer",
                    models.TextField(
                        blank=True, null=True, verbose_name="ответ сервера"
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="messaging.mailing",
                        verbose_name="рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "попытка",
                "verbose_name_plural": "попытки",
            },
        ),
    ]
