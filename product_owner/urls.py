from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from . views import AddExam, DeleteQuestion, IndexView, IndexViewDelete, ShowAnswer

urlpatterns = [
    path('home', login_required(AddExam.as_view())),
    path('delete-question/<int:pk>', login_required(DeleteQuestion.as_view())),
    path('index', login_required(IndexView.as_view())),
    path('index/<int:pk>', login_required(IndexViewDelete.as_view())),
    path('all-answers', login_required(ShowAnswer.as_view())),
    path('edit/<int:pk>', login_required(AddExam.as_view()))
]
