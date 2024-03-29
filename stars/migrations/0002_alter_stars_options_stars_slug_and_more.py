# Generated by Django 4.2.1 on 2024-03-11 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stars", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stars",
            options={"ordering": ["-time_create"]},
        ),
        migrations.AddField(
            model_name="stars",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=255),
        ),
        migrations.AddIndex(
            model_name="stars",
            index=models.Index(
                fields=["-time_create"], name="stars_stars_time_cr_e8721e_idx"
            ),
        ),
    ]
