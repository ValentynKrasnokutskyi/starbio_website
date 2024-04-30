# Generated by Django 4.2.1 on 2024-04-29 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stars", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stars",
            name="author",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="stars",
            name="cat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="posts",
                to="stars.category",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="stars",
            name="spouse",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="star",
                to="stars.spouse",
                verbose_name="Spouse",
            ),
        ),
        migrations.AddField(
            model_name="stars",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tags", to="stars.tagpost", verbose_name="Tags"
            ),
        ),
        migrations.AddIndex(
            model_name="stars",
            index=models.Index(
                fields=["-time_create"], name="stars_stars_time_cr_e8721e_idx"
            ),
        ),
    ]