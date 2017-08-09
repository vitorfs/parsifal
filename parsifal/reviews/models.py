# coding: utf-8

import datetime

from django.utils import timezone
from django.utils.html import escape
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from parsifal.library.models import Document


class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Source'
        verbose_name_plural = u'Sources'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def set_url(self, value):
        if 'http://' not in value and 'https://' not in value and len(value) > 0:
            self.url = u'http://{0}'.format(value)
        else:
            self.url = value


class Review(models.Model):
    UNPUBLISHED = u'U'
    PUBLISHED = u'P'
    REVIEW_STATUS = (
        (UNPUBLISHED, u'Unpublished'),
        (PUBLISHED, u'Published'),
        )

    name = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    objective = models.TextField(max_length=1000)
    sources = models.ManyToManyField(Source)
    status = models.CharField(max_length=1, choices=REVIEW_STATUS, default=UNPUBLISHED)
    co_authors = models.ManyToManyField(User, related_name='co_authors')
    quality_assessment_cutoff_score = models.FloatField(default=0.0)
    population = models.CharField(max_length=200, blank=True)
    intervention = models.CharField(max_length=200, blank=True)
    comparison = models.CharField(max_length=200, blank=True)
    outcome = models.CharField(max_length=200, blank=True)
    context = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = u'Review'
        verbose_name_plural = u'Reviews'
        unique_together = (('name', 'author'),)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('review', args=(str(self.author.username), str(self.name)))

    def get_questions(self):
        questions = Question.objects.filter(review__id=self.id)
        return questions

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

    def get_latest_source_search_strings(self):
        return self.searchsession_set.exclude(source=None).order_by('source__name')

    def get_source_articles(self, source_id=None):
        queryset = Article.objects \
            .filter(review__id=self.id) \
            .select_related('created_by__profile')

        if source_id is not None:
            queryset = queryset.filter(source__id=source_id)
        return queryset

    def get_duplicate_articles(self):
        articles = Article.objects.filter(review__id=self.id).exclude(status=Article.DUPLICATED).order_by('title')
        grouped_articles = dict()

        for article in articles:
            slug = slugify(article.title)
            if slug not in grouped_articles.keys():
                grouped_articles[slug] = { 'size': 0, 'articles': list() }
            grouped_articles[slug]['size'] += 1
            grouped_articles[slug]['articles'].append(article)

        duplicates = list()
        for slug, data in grouped_articles.iteritems():
            if data['size'] > 1:
                duplicates.append(data['articles'])

        return duplicates

    def get_accepted_articles(self):
        return Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)

    def get_final_selection_articles(self):
        accepted_articles = Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)
        if self.has_quality_assessment_checklist() and self.quality_assessment_cutoff_score > 0.0:
            articles = accepted_articles
            for article in accepted_articles:
                if article.get_score() <= self.quality_assessment_cutoff_score:
                    articles = articles.exclude(id=article.id)
            return articles
        else:
            return accepted_articles

    def has_quality_assessment_checklist(self):
        has_questions = self.qualityquestion_set.exists()
        has_answers = self.qualityanswer_set.exists()
        return has_questions and has_answers

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
    review = models.ForeignKey(Review, related_name='research_questions')
    question = models.CharField(max_length=500)
    parent_question = models.ForeignKey('self', null=True, related_name='+')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Question'
        verbose_name_plural = u'Questions'
        ordering = ('order',)

    def __unicode__(self):
        return self.question

    def get_child_questions(self):
        return Question.objects.filter(parent_question=self)


class SelectionCriteria(models.Model):
    INCLUSION = u'I'
    EXCLUSION = u'E'
    SELECTION_TYPES = (
        (INCLUSION, u'Inclusion'),
        (EXCLUSION, u'Exclusion'),
        )

    review = models.ForeignKey(Review)
    criteria_type = models.CharField(max_length=1, choices=SELECTION_TYPES)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = u'Selection Criteria'
        verbose_name_plural = u'Selection Criterias'
        ordering = ('description',)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description[:200]
        super(SelectionCriteria, self).save(*args, **kwargs)


class SearchSession(models.Model):
    review = models.ForeignKey(Review)
    source = models.ForeignKey(Source, null=True)
    search_string = models.TextField(max_length=10000)
    version = models.IntegerField(default=1)

    def __unicode__(self):
        return self.search_string

    def search_string_as_html(self):
        escaped_string = escape(self.search_string)
        html = escaped_string.replace(' OR ', ' <strong>OR</strong> ').replace(' AND ', ' <strong>AND</strong> ')
        return html


def search_result_file_upload_to(instance, filename):
    return u'reviews/{0}/search_result/'.format(instance.review.pk)

class SearchResult(models.Model):
    review = models.ForeignKey(Review)
    source = models.ForeignKey(Source)
    search_session = models.ForeignKey(SearchSession, null=True)
    imported_file = models.FileField(upload_to=search_result_file_upload_to, null=True)
    documents = models.ManyToManyField(Document)


class StudySelection(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User, null=True)
    has_finished = models.BooleanField(default=False)

    def __unicode__(self):
        if self.user:
            selection = u'{0}\'s Selection'.format(self.user.username)
        else:
            selection = u'Final Selection'
        return u'{0} ({1})'.format(selection, self.review.title)


class Study(models.Model):
    UNCLASSIFIED = u'U'
    REJECTED = u'R'
    ACCEPTED = u'A'
    DUPLICATED = u'D'
    STUDY_STATUS = (
        (UNCLASSIFIED, u'Unclassified'),
        (REJECTED, u'Rejected'),
        (ACCEPTED, u'Accepted'),
        (DUPLICATED, u'Duplicated'),
        )
    study_selection = models.ForeignKey(StudySelection, related_name=u'studies')
    document = models.ForeignKey(Document)
    source = models.ForeignKey(Source, null=True)
    status = models.CharField(max_length=1, choices=STUDY_STATUS, default=UNCLASSIFIED)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(max_length=2000, blank=True, null=True)


class Article(models.Model):
    UNCLASSIFIED = u'U'
    REJECTED = u'R'
    ACCEPTED = u'A'
    DUPLICATED = u'D'
    ARTICLE_STATUS = (
        (UNCLASSIFIED, u'Unclassified'),
        (REJECTED, u'Rejected'),
        (ACCEPTED, u'Accepted'),
        (DUPLICATED, u'Duplicated'),
        )

    review = models.ForeignKey(Review)
    bibtex_key = models.CharField(max_length=100)
    title = models.CharField(max_length=1000, null=True, blank=True)
    author = models.CharField(max_length=1000, null=True, blank=True)
    journal = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    source = models.ForeignKey(Source, null=True)
    pages = models.CharField(max_length=20, null=True, blank=True)
    volume = models.CharField(max_length=100, null=True, blank=True)
    abstract = models.TextField(max_length=4000, null=True, blank=True)
    document_type = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=UNCLASSIFIED)
    comments = models.TextField(max_length=2000, null=True, blank=True)
    doi = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    affiliation = models.CharField(max_length=500, null=True, blank=True)
    author_keywords = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    issn = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    finished_data_extraction = models.BooleanField(default=False)
    selection_criteria = models.ForeignKey(SelectionCriteria, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='articles_created', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='articles_updated', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

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

    def get_status_html(self):
        label = { Article.UNCLASSIFIED: 'default', Article.REJECTED: 'danger', Article.ACCEPTED: 'success', Article.DUPLICATED: 'warning' }
        return u'<span class="label label-{0}">{1}</span>'.format(label[self.status], self.get_status_display())


class Keyword(models.Model):
    POPULATION = u'P'
    INTERVENTION = u'I'
    COMPARISON = u'C'
    OUTCOME = u'O'
    RELATED_TO = (
        (POPULATION, u'Population'),
        (INTERVENTION, u'Intervention'),
        (COMPARISON, u'Comparison'),
        (OUTCOME, u'Outcome'),
        )

    review = models.ForeignKey(Review, related_name='keywords')
    description = models.CharField(max_length=200)
    synonym_of = models.ForeignKey('self', null=True, related_name='synonyms')
    related_to = models.CharField(max_length=1, choices=RELATED_TO, blank=True)

    class Meta:
        verbose_name = u'Keyword'
        verbose_name_plural = u'Keywords'
        ordering = ('description',)

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
        verbose_name = 'Quality Assessment Answer'
        verbose_name_plural = 'Quality Assessment Answers'
        ordering = ('-weight',)

    def __unicode__(self):
        return self.description


class QualityQuestion(models.Model):
    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Quality Assessment Question'
        verbose_name_plural = 'Quality Assessment Questions'
        ordering = ('order',)

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
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Data Extraction Field'
        verbose_name_plural = 'Data Extraction Fields'
        ordering = ('order',)

    def get_select_values(self):
        return DataExtractionLookup.objects.filter(field__id=self.id)

    def is_select_field(self):
        return self.field_type in (self.SELECT_ONE_FIELD, self.SELECT_MANY_FIELD)


class DataExtractionLookup(models.Model):
    field = models.ForeignKey(DataExtractionField)
    value = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'Lookup Value'
        verbose_name_plural = 'Lookup Values'
        ordering = ('value',)

    def __unicode__(self):
        return self.value


class DataExtraction(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article)
    field = models.ForeignKey(DataExtractionField)
    value = models.TextField(blank=True, null=True)
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
        if self.field.field_type:
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
        return self._get_string_value()

    def get_date_value_as_string(self):
        try:
            value = self.get_value()
            return value.strftime('%m/%d/%Y')
        except Exception, e:
            return ''
