from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.reviews.decorators import author_required, main_author_required
from parsifal.apps.reviews.forms import CreateReviewForm, ReviewForm
from parsifal.apps.reviews.models import Review


def reviews(request, username):
    user = get_object_or_404(User, username__iexact=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = user.profile.get_followers_count()
    following_count = user.profile.get_following_count()

    user_reviews = user.profile.get_reviews()

    pending_invites = user.invites_received.filter(status=InviteStatus.PENDING)
    pending_invites_count = pending_invites.count()

    return render(
        request,
        "reviews/reviews.html",
        {
            "user_reviews": user_reviews,
            "page_user": user,
            "is_following": is_following,
            "following_count": following_count,
            "followers_count": followers_count,
            "pending_invites": pending_invites,
            "pending_invites_count": pending_invites_count,
        },
    )


@login_required
def new(request):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user

            name = slugify(form.instance.title)
            if not name:
                name = "literature-review"
            unique_name = name
            i = 0
            while Review.objects.filter(name=unique_name, author__username=request.user.username):
                i = i + 1
                unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, "Review created successfully.")
            return redirect(r("review", args=(review.author.username, review.name)))
    else:
        form = CreateReviewForm()
    return render(request, "reviews/new.html", {"form": form})


@author_required
@login_required
def review(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, "Review was saved successfully.")
            return redirect(r("review", args=(review.author.username, review.name)))
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review.html", {"review": review, "form": form})


@main_author_required
@login_required
@require_POST
def add_author_to_review(request):
    emails = request.POST.getlist("users")
    review_id = request.POST.get("review-id")
    review = get_object_or_404(Review, pk=review_id)
    authors_added = []
    authors_invited = []

    inviter_name = request.user.profile.get_screen_name()

    for email in emails:
        try:
            user = User.objects.get(email__iexact=email)
            if user.id != review.author.id:
                authors_added.append(user.profile.get_screen_name())
                review.co_authors.add(user)
        except User.DoesNotExist:
            authors_invited.append(email)

            subject = "{0} wants to add you as co-author on the systematic literature review {1}".format(
                inviter_name, review.title
            )
            from_email = "{0} via Parsifal <noreply@parsif.al>".format(inviter_name)

            text_content = """Hi {0},
            {1} invited you to a Parsifal Systematic Literature Review called "{2}".
            View the review at https://parsif.al/{3}/{4}/""".format(
                email, inviter_name, review.title, request.user.username, review.name
            )

            html_content = """<p>Hi {0},</p>
            <p>{1} invited you to a Parsifal Systematic Literature Review called "{2}".</p>
            <p>View the review at https://parsif.al/{3}/{4}/</p>
            <p>Sincerely,</p>
            <p>The Parsifal Team</p>""".format(
                email, inviter_name, review.title, request.user.username, review.name
            )

            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    review.save()

    if not authors_added and not authors_invited:
        messages.info(request, "No author invited or added to the review. Nothing really changed.")

    if authors_added:
        messages.success(request, "The authors {0} were added successfully.".format(", ".join(authors_added)))

    if authors_invited:
        messages.success(request, "{0} were invited successfully.".format(", ".join(authors_invited)))

    return redirect(r("review", args=(review.author.username, review.name)))


@main_author_required
@login_required
@require_POST
def remove_author_from_review(request):
    try:
        author_id = request.POST.get("user-id")
        review_id = request.POST.get("review-id")
        author = User.objects.get(pk=author_id)
        review = Review.objects.get(pk=review_id)
        review.co_authors.remove(author)
        review.save()
        return HttpResponse()
    except Exception:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_description(request):
    try:
        review_id = request.POST["review-id"]
        description = request.POST["description"]
        review = Review.objects.get(pk=review_id)
        if len(description) > 500:
            return HttpResponseBadRequest(
                "The review description should not exceed 500 characters. The given description have %s characters."
                % len(description)
            )
        else:
            review.description = description
            review.save()
            return HttpResponse("Your review has been saved successfully!")
    except Exception:
        return HttpResponseBadRequest()


@author_required
@login_required
def leave(request):
    review_id = request.POST.get("review-id")
    review = get_object_or_404(Review, pk=review_id)
    review.co_authors.remove(request.user)
    review.save()
    messages.add_message(request, messages.SUCCESS, "You successfully left the review {0}.".format(review.title))
    return redirect("/" + request.user.username + "/")
