# Generated by Django 4.2.1 on 2023-06-05 03:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_sharedresourcetoken_object_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sharedresourcetoken",
            name="token",
            field=models.CharField(
                db_index=True,
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_token",
                        message="Token must be 50 characters long and URL safe.",
                        regex="^[\\w-]{,50}$",
                    )
                ],
            ),
        ),
    ]
