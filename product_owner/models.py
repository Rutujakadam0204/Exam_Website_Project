from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    marks_out_of = models.IntegerField(null=True, blank=True)


class Question(models.Model):
    experiment = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=100000, blank=True)
    question_display_type = models.CharField(max_length=100, blank=True)
    quest_image = models.FileField(upload_to="question", blank=True)
    answer = models.TextField(max_length=99999999, blank=True)


class IndexModel(models.Model):
    exp = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=100000, blank=True)