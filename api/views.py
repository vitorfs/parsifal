from django.contrib.auth.models import User, Group
from reviews.models import Review, Source, Question, SelectionCriteria, Article, Keyword
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ReviewSerializer, SourceSerializer, \
    QuestionSerializer, SelectionCriteriaSerializer, ArticleSerializer, KeywordSerializer
from rest_framework.decorators import api_view

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class SelectionCriteriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SelectionCriteria.objects.all()
    serializer_class = SelectionCriteriaSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class KeywordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
