from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'reviews.views.index'),
    (r'^reviews/new/$', 'reviews.views.new'),
    (r'^reviews/review/$', 'reviews.views.review'),
    (r'^login/$', 'core.views.login'),
    (r'^logout/$', 'core.views.logout'),
)
