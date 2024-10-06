# Generated by Django 5.1.1 on 2024-10-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                ("city", models.TextField()),
                ("email_address", models.TextField()),
                ("profile_image_url", models.TextField()),
            ],
        ),
    ]