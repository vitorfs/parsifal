from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'core.views.home'),
    #(r'^reviews/$', 'reviews.views.reviews'),
    (r'^reviews/new/$', 'reviews.views.new'),
    (r'^reviews/review/$', 'reviews.views.review'),
    (r'^signin/$', 'core.views.signin'),
    (r'^signout/$', 'core.views.signout'),
    (r'^(?P<username>\w{1,50})/$', 'reviews.views.reviews'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
