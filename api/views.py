from django.contrib.auth.models import User
from reviews.models import Review, Source, Question, SelectionCriteria, Article, Keyword
from api.serializers import UserSerializer, ReviewSerializer, SourceSerializer, QuestionSerializer, SelectionCriteriaSerializer, ArticleSerializer, KeywordSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

class ArticleList(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_fields = ('review', 'status', 'source')

class KeywordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
