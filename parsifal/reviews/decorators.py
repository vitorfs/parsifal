from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404

from parsifal.reviews.models import Review


def main_author_required(f):
    def wrap(request, *args, **kwargs):
        if 'review_name' in kwargs and 'username' in kwargs:
            try:
                review = Review.objects.get(name=kwargs['review_name'], author__username__iexact=kwargs['username'])
                if review.author.id == request.user.id:
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            except Review.DoesNotExist:
                raise Http404
        else:
            try:
                review_id = request.POST['review-id']
            except:
                try:
                    review_id = request.GET['review-id']
                except:
                    return HttpResponseBadRequest()

            review = Review.objects.get(pk=review_id)
            if review.author.id == request.user.id:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def author_required(f):
    def wrap(request, *args, **kwargs):
        if 'review_name' in kwargs and 'username' in kwargs:
            try:
                review = Review.objects.get(name=kwargs['review_name'], author__username__iexact=kwargs['username'])
                if review.is_author_or_coauthor(request.user):
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            except Review.DoesNotExist:
                raise Http404
        else:
            try:
                review_id = request.POST['review-id']
            except:
                try:
                    review_id = request.GET['review-id']
                except:
                    return HttpResponseBadRequest()
            review = Review.objects.get(pk=review_id)
            if review.is_author_or_coauthor(request.user):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap