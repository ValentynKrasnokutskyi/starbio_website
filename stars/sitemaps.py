from django.contrib.sitemaps import Sitemap

from stars.models import Category, Stars


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Stars.published.all()

    def lastmod(self, obj):
        return obj.time_update


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Category.objects.all()
