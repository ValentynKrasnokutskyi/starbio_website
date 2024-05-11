from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
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

    title = models.CharField(max_length=255, verbose_name='Title', validators=[
        MinLengthValidator(1, message='Minimum 1 characters'),
        MaxLengthValidator(50, message='Maximum 50 characters'),
                            ])  # Title of the star
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Slug', validators=[
        MinLengthValidator(1, message='Minimum 1 characters'),
        MaxLengthValidator(50, message='Maximum 50 characters'),
                            ])  # Unique slug for URLs
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Photo")
    content = models.TextField(blank=True, verbose_name='Article text')  # Content of the star
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')  # Date and time of creation
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")  # Date and time of last update
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Status')  # Status of publication
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts',
                            verbose_name='Category')  # Category of the star
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',
                                  verbose_name='Tags')  # Tags associated with the star
    spouse = models.OneToOneField('Spouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='star',
                                  verbose_name='Spouse')  # Spouse of the star
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)  # Author of the article

    objects = models.Manager()
    published = PublishedModel()  # Custom manager for published stars

    class Meta:
        verbose_name = 'Star'
        verbose_name_plural = 'Stars'
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
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category')  # Name of the category
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # Unique slug for URLs

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

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
