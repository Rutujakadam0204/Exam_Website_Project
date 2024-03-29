from django.db import models
from django.contrib.auth.models import User
from product_owner.models import Question, Exam
from login_registration.models import CollegeRegistration


class GivenExam(models.Model):
    college = models.ForeignKey(CollegeRegistration, on_delete=models.CASCADE, blank=True, null=True)
    exam_type = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    exam_date = models.DateTimeField(blank=True, null=True)
    experiments = models.CharField(null=True, blank=True, max_length=10000)
    student_roll = models.CharField(blank=True, max_length=100)
    answer_pdf_file = models.FileField(upload_to='answer_pdf', null=True, blank=True)
    exam_submitted = models.BooleanField(default=False)
    marks_scored = models.IntegerField(null=True)


class Answer(models.Model):
    exam_details = models.ForeignKey(GivenExam, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name='question_answer')
    text = models.TextField(blank=True, max_length=1000000)
