from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):  # Custom manager for published models
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Stars.Status.PUBLISHED)


class Stars(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Draft'
        PUBLISHED = 1, 'Published'

    title = models.CharField(max_length=255)  # Title of the star
    slug = models.SlugField(max_length=255, db_index=True, unique=True)  # Unique slug for URLs
    content = models.TextField(blank=True)  # Content of the star
    time_create = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    time_update = models.DateTimeField(auto_now=True)  # Date and time of last update
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)  # Status of publication

    objects = models.Manager()
    published = PublishedModel()  # Custom manager for published stars

    class Meta:
        ordering = ['-time_create']  # Ordering stars by creation time in descending order
        indexes = [
            models.Index(fields=['-time_create']),  # Index for faster querying by creation time
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})  # URL pattern for accessing a star detail view
