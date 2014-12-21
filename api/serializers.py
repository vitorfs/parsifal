from django.contrib.auth.models import User, Group
from reviews.models import Review, Source, Question, SelectionCriteria, Article, Keyword
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question

class SelectionCriteriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SelectionCriteria

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword