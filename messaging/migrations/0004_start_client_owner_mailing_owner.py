# Generated by Django 5.1.2 on 2024-11-10 12:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0003_remove_client_owner_remove_mailing_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Start",
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
                    models.CharField(
                        help_text="Введите стартовые позиции",
                        max_length=100,
                        verbose_name="Стартовая позиция",
                    ),
                ),
            ],
            options={
                "verbose_name": "Старт",
                "verbose_name_plural": "Старты",
            },
        ),
        migrations.AddField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
    ]
