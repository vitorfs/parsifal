from django.contrib.sitemaps import Sitemap

from parsifal.apps.blog.models import Entry


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(status=Entry.PUBLISHED).order_by("-start_publication")

    def lastmod(self, obj):
        return obj.last_update
