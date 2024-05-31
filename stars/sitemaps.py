from django.contrib.sitemaps import Sitemap
from stars.models import Category, Stars


class PostSitemap(Sitemap):
    """
    Sitemap for posts (stars).
    """

    changefreq = "monthly"  # How often the page is likely to change
    priority = 0.9  # Priority of the page compared to other pages

    def items(self):
        """
        Returns the queryset of items to include in this sitemap.
        """
        return Stars.published.all()  # Return only published stars

    def lastmod(self, obj):
        """
        Returns the last modification time for the given object.
        """
        return obj.time_update  # Return the last update time of the star


class CategorySitemap(Sitemap):
    """
    Sitemap for categories.
    """

    changefreq = "monthly"  # How often the page is likely to change
    priority = 0.9  # Priority of the page compared to other pages

    def items(self):
        """
        Returns the queryset of items to include in this sitemap.
        """
        return Category.objects.all()  # Return all categories
