# Generated by Django 4.2 on 2023-05-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gifs", "0006_reaction_remove_gif_reactions_alter_gif_uploader_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reaction",
            name="is_nsfw",
            field=models.BooleanField(
                default=False, help_text="Wether the reaction is NSFW or not."
            ),
        ),
    ]
