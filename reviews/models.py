# coding: utf-8

import datetime
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    def set_url(self, value):
        if "http://" not in value and "https://" not in value and len(value) > 0:
            self.url = "http://" + str(value)
        else:
            self.url = value


class Review(models.Model):
    UNPUBLISHED = 'U'
    PUBLISHED = 'P'
    REVIEW_STATUS = (
        (UNPUBLISHED, 'Unpublished'),
        (PUBLISHED, 'Published'),
        )

    SINGLE_FORM = 'S'
    MULTIPLE_FORMS = 'M'
    CONDUCTING_STRATEGY = (
        (SINGLE_FORM, 'Single Form'),
        (MULTIPLE_FORMS, 'Multiple Forms'),
        )

    name = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField()
    objective = models.TextField(max_length=1000)
    sources = models.ManyToManyField(Source)
    status = models.CharField(max_length=1, choices=REVIEW_STATUS, default=UNPUBLISHED)
    co_authors = models.ManyToManyField(User, related_name="co_authors")
    quality_assessment_cutoff_score = models.FloatField(default=0.0)
    study_selection_strategy = models.CharField(max_length=1, choices=CONDUCTING_STRATEGY, default=SINGLE_FORM)
    quality_assessment_strategy = models.CharField(max_length=1, choices=CONDUCTING_STRATEGY, default=SINGLE_FORM)
    data_extraction_strategy = models.CharField(max_length=1, choices=CONDUCTING_STRATEGY, default=SINGLE_FORM)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __unicode__(self):
        return self.name

    def save(self):
        self.last_update = datetime.datetime.now()
        super(Review, self).save()

    def get_questions(self):
        questions = Question.objects.filter(review__id=self.id)
        return questions

    def get_main_question(self):
        try:
            question = Question.objects.filter(review__id=self.id, question_type='M')[:1].get()
        except Question.DoesNotExist:
            question = Question()
        return question

    def get_secondary_questions(self):
        return Question.objects.filter(review__id=self.id, question_type='S')

    def get_inclusion_criterias(self):
        return SelectionCriteria.objects.filter(review__id=self.id, criteria_type='I')

    def get_exclusion_criterias(self):
        return SelectionCriteria.objects.filter(review__id=self.id, criteria_type='E')    

    def get_keywords(self):
        return Keyword.objects.filter(review__id=self.id, synonym_of=None)

    def is_author_or_coauthor(self, user):
        if user.id == self.author.id:
            return True
        for co_author in self.co_authors.all():
            if user.id == co_author.id:
                return True
        return False

    def get_generic_search_string(self):
        try:
            search_string = SearchSession.objects.filter(review__id=self.id, source=None)[:1].get()
        except SearchSession.DoesNotExist:
            search_string = SearchSession(review=self)
        return search_string

    def get_source_articles(self, source_id=None):
        if source_id is None:
            return Article.objects.filter(review__id=self.id)
        else:
            return Article.objects.filter(review__id=self.id, source__id=source_id)

    def get_duplicate_articles(self):
        articles = Article.objects.filter(review__id=self.id).exclude(status=Article.DUPLICATED)

        duplicates = []
        duplicates_control_id = []

        for i in range(0, len(articles)):
            temp_duplicates = []
            for j in range(0, len(articles)):
                if i != j and articles[i].title.lower().strip() == articles[j].title.lower().strip():
                    if articles[j].id not in duplicates_control_id:
                        temp_duplicates.append(articles[j])
                        duplicates_control_id.append(articles[j].id)
            if len(temp_duplicates) > 0:
                duplicates_control_id.append(articles[i].id)
                temp_duplicates.append(articles[i])
                duplicates.append(temp_duplicates)

        return duplicates

    def get_accepted_articles(self):
        return Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)

    def get_final_selection_articles(self):
        accepted_articles = Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)
        if self.quality_assessment_cutoff_score > 0.0:
            articles = accepted_articles
            for article in accepted_articles:
                if article.get_score() <= self.quality_assessment_cutoff_score:
                    articles = articles.exclude(id=article.id)
            return articles
        else:
            return accepted_articles

    def get_data_extraction_fields(self):
        return DataExtractionField.objects.filter(review__id=self.id)

    def get_quality_assessment_questions(self):
        return QualityQuestion.objects.filter(review__id=self.id)

    def get_quality_assessment_answers(self):
        return QualityAnswer.objects.filter(review__id=self.id)

    def calculate_quality_assessment_max_score(self):
        try:
            questions_count = QualityQuestion.objects.filter(review__id=self.id).count()
            higher_weight_answer = QualityAnswer.objects.filter(review__id=self.id).order_by('-weight')[:1].get()
            if questions_count and higher_weight_answer:
                return questions_count * higher_weight_answer.weight
            else:
                return 0.0
        except:
            return 0.0


class Question(models.Model):
    MAIN = 'M'
    SECONDARY = 'S'
    QUESTION_TYPES = (
        (MAIN, 'Main'),
        (SECONDARY, 'Secondary'),
        )

    review = models.ForeignKey(Review)
    question = models.CharField(max_length=500)
    population = models.CharField(max_length=200)
    intervention = models.CharField(max_length=200)
    comparison = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __unicode__(self):
        return self.question


class SelectionCriteria(models.Model):
    INCLUSION = 'I'
    EXCLUSION = 'E'
    SELECTION_TYPES = (
        (INCLUSION, 'Inclusion'),
        (EXCLUSION, 'Exclusion'),
        )

    review = models.ForeignKey(Review)
    criteria_type = models.CharField(max_length=1, choices=SELECTION_TYPES)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Selection Criteria"
        verbose_name_plural = "Selection Criterias"
        ordering = ("description",)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description[:200]
        super(SelectionCriteria, self).save(*args, **kwargs)


class SearchSession(models.Model):
    review = models.ForeignKey(Review)
    source = models.ForeignKey(Source, null=True)
    search_string = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.search_string


class Article(models.Model):
    UNCLASSIFIED = 'U'
    REJECTED = 'R'
    ACCEPTED = 'A'
    DUPLICATED = 'D'
    ARTICLE_STATUS = (
        (UNCLASSIFIED, 'Unclassified'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (DUPLICATED, 'Duplicated'),
        )

    review = models.ForeignKey(Review)
    bibtex_key = models.CharField(max_length=100)
    title = models.CharField(max_length=1000, blank=True)
    author = models.CharField(max_length=1000, blank=True)
    journal = models.CharField(max_length=1000, blank=True)
    year = models.CharField(max_length=10, blank=True)
    source = models.ForeignKey(Source, null=True)
    pages = models.CharField(max_length=20, blank=True)
    volume = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=1000, blank=True)
    abstract = models.TextField(max_length=4000, blank=True)
    document_type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=UNCLASSIFIED)
    comments = models.TextField(max_length=4000, blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __unicode__(self):
        return self.title

    def get_score(self):
        score = QualityAssessment.objects.filter(article__id=self.id).aggregate(Sum('answer__weight'))
        if score['answer__weight__sum'] == None:
            return 0.0
        return score['answer__weight__sum']

    def get_quality_assesment(self):
        quality_assessments = QualityAssessment.objects.filter(article__id=self.id)
        return quality_assessments


class Keyword(models.Model):
    review = models.ForeignKey(Review)
    description = models.CharField(max_length=200)
    synonym_of = models.ForeignKey("self", null=True)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"
        ordering = ("description",)
            
    def __unicode__(self):
        return self.description
        
    def save(self, *args, **kwargs):
        self.description = self.description[:200]
        super(Keyword, self).save(*args, **kwargs)

    def get_synonyms(self):
        return Keyword.objects.filter(review__id=self.review.id, synonym_of__id=self.id)


class QualityAnswer(models.Model):
    SUGGESTED_ANSWERS = (
        ('Yes', 1.0), 
        ('Partially', 0.5), 
        ('No', 0.0)
        )

    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        verbose_name = "Quality Assessment Answer"
        verbose_name_plural = "Quality Assessment Answers"
        ordering = ("-weight",)

    def __unicode__(self):
        return self.description


class QualityQuestion(models.Model):
    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Quality Assessment Question"
        verbose_name_plural = "Quality Assessment Questions"

    def __unicode__(self):
        return self.description


class QualityAssessment(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article)
    question = models.ForeignKey(QualityQuestion)
    answer = models.ForeignKey(QualityAnswer, null=True)

    def __unicode__(self):
        return str(self.article.id) + ' ' + str(self.question.id)


class DataExtractionField(models.Model):
    BOOLEAN_FIELD = 'B'
    STRING_FIELD = 'S'
    FLOAT_FIELD = 'F'
    INTEGER_FIELD = 'I'
    DATE_FIELD = 'D'
    SELECT_ONE_FIELD = 'O'
    SELECT_MANY_FIELD = 'M'
    FIELD_TYPES = (
        (BOOLEAN_FIELD, 'Boolean Field'),
        (STRING_FIELD, 'String Field'),
        (FLOAT_FIELD, 'Float Field'),
        (INTEGER_FIELD, 'Integer Field'),
        (DATE_FIELD, 'Date Field'),
        (SELECT_ONE_FIELD, 'Select One Field'),
        (SELECT_MANY_FIELD, 'Select Many Field'),
        )

    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES)

    def get_select_values(self):
        return DataExtractionLookup.objects.filter(field__id=self.id)

    def is_select_field(self):
        return self.field_type in (self.SELECT_ONE_FIELD, self.SELECT_MANY_FIELD)


class DataExtractionLookup(models.Model):
    field = models.ForeignKey(DataExtractionField)
    value = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Lookup Value"
        verbose_name_plural = "Lookup Values"
        ordering = ("value",)

    def __unicode__(self):
        return self.value


class DataExtraction(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article)
    field = models.ForeignKey(DataExtractionField)
    value = models.CharField(max_length=1000, blank=True)
    select_values = models.ManyToManyField(DataExtractionLookup)

    def _set_boolean_value(self, value):
        if value:
            if value in ['True', 'False']:
                self.value = value
            else:
                raise ValueError('Expected values: "True" or "False"')
        else:
            self.value = ''

    def _set_string_value(self, value):
        try:
            self.value = value.strip()
        except Exception, e:
            raise e

    def _set_float_value(self, value):
        try:
            if value:
                _value = value.replace(',', '.')
                self.value = float(_value)
            else:
                self.value = ''
        except:
            raise Exception('Invalid input for ' + self.field.description + ' field. Expected value: floating point number. Please use dot instead of comma.')

    def _set_integer_value(self, value):
        try:
            if value:
                _value = value.replace(',', '.')
                self.value = int(float(_value))
            else:
                self.value = ''
        except:
            raise Exception('Invalid input for ' + self.field.description + ' field. Expected value: integer number.')

    def _set_date_value(self, value):
        try:
            if value:
                _value = datetime.datetime.strptime(value, '%m/%d/%Y').date()
                self.value = str(_value)
            else:
                self.value = ''
        except:
            raise Exception('Invalid input for ' + self.field.description + ' field. Expected value: date. Please use the format MM/DD/YYYY.')

    def _set_select_one_value(self, value):
        try:
            self.value = ''
            self.select_values.clear()
            if value:
                _value = DataExtractionLookup.objects.get(pk=value)
                self.select_values.add(_value)
        except Exception, e:
            raise e

    def _set_select_many_value(self, value):
        try:
            self.value = ''
            _value = DataExtractionLookup.objects.get(pk=value)
            if _value in self.select_values.all():
                self.select_values.remove(_value)
            else:
                self.select_values.add(_value)
        except Exception, e:
            raise e

    def set_value(self, value):
        set_value_functions = {
            DataExtractionField.BOOLEAN_FIELD: self._set_boolean_value,
            DataExtractionField.STRING_FIELD: self._set_string_value,
            DataExtractionField.FLOAT_FIELD: self._set_float_value,
            DataExtractionField.INTEGER_FIELD: self._set_integer_value,
            DataExtractionField.DATE_FIELD: self._set_date_value,
            DataExtractionField.SELECT_ONE_FIELD: self._set_select_one_value,
            DataExtractionField.SELECT_MANY_FIELD: self._set_select_many_value,
        }
        set_value_functions[self.field.field_type](value[:1000])

    def _get_boolean_value(self):
        try:
            if self.value == 'True':
                return True
            elif self.value == 'False':
                return False
            else:
                return ''
        except Exception, e:
            return ''

    def _get_string_value(self):
        return self.value

    def _get_float_value(self):
        try:
            return float(self.value)
        except Exception, e:
            return ''

    def _get_integer_value(self):
        try:
            return int(self.value)
        except Exception, e:
            return ''

    def _get_date_value(self):
        try:
            if self.value != '':
                return datetime.datetime.strptime(self.value, '%Y-%m-%d').date()
            else:
                return ''
        except Exception, e:
            return ''

    def _get_select_one_value(self):
        try:
            return self.select_values.all()[0]
        except Exception, e:
            return None

    def _get_select_many_value(self):
        try:
            return self.select_values.all()
        except Exception, e:
            return []

    def get_value(self):
        get_value_functions = {
            DataExtractionField.BOOLEAN_FIELD: self._get_boolean_value,
            DataExtractionField.STRING_FIELD: self._get_string_value,
            DataExtractionField.FLOAT_FIELD: self._get_float_value,
            DataExtractionField.INTEGER_FIELD: self._get_integer_value,
            DataExtractionField.DATE_FIELD: self._get_date_value,
            DataExtractionField.SELECT_ONE_FIELD: self._get_select_one_value,
            DataExtractionField.SELECT_MANY_FIELD: self._get_select_many_value,
        }
        return get_value_functions[self.field.field_type]()

    def get_date_value_as_string(self):
        try:
            value = self.get_value()
            return value.strftime('%m/%d/%Y')
        except Exception, e:
            return ''