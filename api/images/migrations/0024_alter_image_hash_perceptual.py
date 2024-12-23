# Generated by Django 4.2.3 on 2023-07-25 05:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0023_image_hash_perceptual"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="hash_perceptual",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=64,
                null=True,
                verbose_name="Perceptual hash",
            ),
        ),
    ]
