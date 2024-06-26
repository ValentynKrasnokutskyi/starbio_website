from django.urls import path, register_converter
from django.views.decorators.cache import cache_page

from . import converters, views

# Register custom converter for four-digit years
register_converter(converters.FourDigitYearConverter, "year4")

# URL patterns
urlpatterns = [
    path("", views.StarsHome.as_view(), name="home"),  # http://127.0.0.1:8000
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("post/<slug:post_slug>/", cache_page(20)(views.ShowPost.as_view()), name="post"),
    path("category/<slug:cat_slug>/", views.StarsCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.TagPostList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
]
