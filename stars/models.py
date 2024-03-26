from django.db import models
from django.urls import reverse


# Custom manager for published models
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Stars.Status.PUBLISHED)


# Model representing a star
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
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')  # Category of the star
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')  # Tags associated with the star
    spouse = models.OneToOneField('Spouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='star')  # Spouse of the star

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


# Model representing a category
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # Name of the category
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # Unique slug for URLs

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})  # URL pattern for accessing a category detail view

    def __str__(self):
        return self.name


# Model representing a tag
class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)  # Tag name
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # Unique slug for URLs

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})  # URL pattern for accessing a tag detail view

    def __str__(self):
        return self.tag


# Model representing a spouse
class Spouse(models.Model):
    name = models.CharField(max_length=100)  # Name of the spouse
    age = models.IntegerField(null=True)  # Age of the spouse
    m_count = models.IntegerField(blank=True, default=0)  # number of marriages of the spouse

    def __str__(self):
        return self.name
