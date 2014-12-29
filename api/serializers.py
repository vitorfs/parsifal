from django.contrib.auth.models import User
from reviews.models import Review, Source, Question, SelectionCriteria, Article, Keyword
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question

class SelectionCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectionCriteria

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword