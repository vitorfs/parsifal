from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from reviews.models import Review
from reviews.decorators import main_author_required, author_required


@login_required
@author_required
def publish(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    return render(request, 'publish/publish.html', { 'review': review })