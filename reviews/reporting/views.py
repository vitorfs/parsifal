# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from reviews.models import *
from reviews.decorators import author_required


@author_required
@login_required
def reporting(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    return render(request, 'reporting/reporting.html', { 'review': review })
