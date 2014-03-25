# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.reporting.views',
    url(r'^articles_selection_chart/$', 'articles_selection_chart', name='articles_selection_chart'),
)