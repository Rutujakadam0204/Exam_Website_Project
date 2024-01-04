from django.shortcuts import render, redirect
from rest_framework.views import APIView
from . models import Question, IndexModel
from django.http import HttpResponseRedirect


class AddExam(APIView):
    def get(self, request):
        data = {
            'questions': Question.objects.all()
        }
        return render(request, 'crud_questions.html', data)

    def post(self, request, pk=None):
        if pk is None:
            Question.objects.create(experiment=request.data['experiment'],
                                    text=request.data['text'],
                                    question_display_type=request.data['question_display_type'],
                                    quest_image=request.data['quest_image'],
                                    answer=request.data['answer']
                                    )
        else:
            Question.objects.filter(id=pk).update(
                experiment=request.data['experiment'],
                text=request.data['text'],
                question_display_type=request.data['question_display_type'],
                quest_image=request.data['quest_image'],
                answer=request.data['answer']
            )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DeleteQuestion(APIView):
    def get(self, request, pk):
        Question.objects.filter(id=pk).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ShowAnswer(APIView):
    def get(self, request):
        data = {
            'questions': Question.objects.all()
        }
        return render(request, 'show_answer.html', data)


class IndexView(APIView):
    def get(self, request):
        data={'index':IndexModel.objects.all().order_by('exp').values()}
        return render(request,'crud.html', data)

    def post(self, request):
        IndexModel.objects.create(exp = request.data['exp'], title = request.data['title'])
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexViewDelete(APIView):
    def get(self, request, pk):
        IndexModel.objects.filter(id=pk).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
