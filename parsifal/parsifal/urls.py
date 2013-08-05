from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'core.views.home'),
    (r'^reviews/$', 'reviews.views.reviews'),
    (r'^reviews/new/$', 'reviews.views.new'),
    (r'^reviews/review/$', 'reviews.views.review'),
    (r'^signin/$', 'core.views.signin'),
    (r'^signout/$', 'core.views.signout'),
)
