# Generated by Django 4.2 on 2023-05-10 02:33

from django.db import migrations, models
import dynamic_filenames
import thumbnails.fields


class Migration(migrations.Migration):
    dependencies = [
        ("gifs", "0001_squashed_0004_alter_gif_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="gif",
            name="aspect_ratio",
            field=models.CharField(
                blank=True,
                help_text="The gif's aspect ratio (w:h).",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="file_size",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="The file size in bytes of the image file.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="frames",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="The amount of frames that the GIF has.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="height",
            field=models.SmallIntegerField(
                default=0, help_text="The gif's height in pixels."
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="mimetype",
            field=models.CharField(
                blank=True,
                help_text="The image's file format.",
                max_length=11,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="orientation",
            field=models.CharField(
                blank=True,
                choices=[
                    ("landscape", "Landscape"),
                    ("portrait", "Portrait"),
                    ("square", "Square"),
                ],
                max_length=9,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gif",
            name="width",
            field=models.SmallIntegerField(
                default=0, help_text="The gif's width in pixels."
            ),
        ),
        migrations.AlterField(
            model_name="gif",
            name="file",
            field=thumbnails.fields.ImageField(
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern="gifs/{uuid:base32}{ext}"
                )
            ),
        ),
    ]
