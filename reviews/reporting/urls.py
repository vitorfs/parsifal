# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.reporting.views',
    url(r'^articles_selection_chart/$', 'articles_selection_chart', name='articles_selection_chart'),
    url(r'^articles_per_year/$', 'articles_per_year', name='articles_per_year'),
)