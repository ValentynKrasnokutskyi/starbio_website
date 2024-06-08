"""
URL configuration for starbio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.defaults import page_not_found

from starbio import settings
#  from starbio import settings
from stars.sitemaps import CategorySitemap, PostSitemap

from rest_framework import routers

from stars.views import StarsViewSet

# Create a router for automatic URL generation for ViewSet
router = routers.DefaultRouter()  # Register the ViewSet for the Stars model
router.register(r'stars', StarsViewSet)

# Define sitemaps for different models
sitemaps = {
    "posts": PostSitemap,
    "cats": CategorySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),  # URL for the admin panel
    path("", include("stars.urls")),  # Include URLs from the stars app
    path("users/", include("users.urls", namespace="users")),  # Include URLs from the users app
    path("__debug__/", include("debug_toolbar.urls")),  # Include URLs for Django Debug Toolbar
    path("social-auth/", include("social_django.urls", namespace="social")),  # Include URLs for social authentication
    path("captcha/", include("captcha.urls")),  # Include URLs for captcha
    path("sitemap.xml", cache_page(3600)(sitemap), {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap",),  # URL for sitemap with 1 hour caching
    path('api/v1/', include(router.urls)),  # URL for API v1, managed by the router
    path('api/v1/drf-auth/', include('rest_framework.urls')),  # URL for built-in DRF authentication
    # Uncommented URLs for individual API views (uncomment if needed)
    # path('api/v1/starslist/', StarsAPIList.as_view()),
    # path('api/v1/starslist/<int:pk>/', StarsAPIUpdate.as_view()),
    # path('api/v1/starsdetail/<int:pk>/', StarsAPIDetailView.as_view()),
]

# Add URLs for serving media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Define handler for 404 error
handler404 = page_not_found

# Admin panel settings
admin.site.site_header = "Administration Panel"
admin.site.index_title = "Celebrities of the world"
