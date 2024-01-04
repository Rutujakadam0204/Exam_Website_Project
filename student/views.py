from django.contrib import messages
from django.shortcuts import render, redirect
from product_owner.models import Question, Exam
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import GivenExam, Answer
from django.db import transaction
from login_registration.models import Profile
from datetime import datetime
from django.http import HttpResponseRedirect

class MyExam(APIView):
    def get(self, request, pk):
        quest = Answer.objects.filter(exam_details__id=pk)
        data = {'quest': quest, 'exam_id': pk}
        return render(request, 'exam_page.html', data)


class MyExamAnswer(APIView):
    def get(self, request, pk):
        if not Answer.objects.filter(id=pk, exam_details__exam_submitted=True).exists():
            Answer.objects.filter(id=pk).update(text=request.GET['answer'])
            return Response({'msg':'Answer submitted successfully !!!'})
        else:
            return Response({'msg':'Answer already recorded'})


class ExamDetails(APIView):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = {'exam_type': Exam.objects.all(),
                'students':Profile.objects.filter(login_allow=True,
                                                  user__groups__name__in=['student'],
                                                  college=profile.college
                                                  )}
        return render(request, 'exam_details.html', data)

    @transaction.atomic()
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        if GivenExam.objects.filter(student=request.user, exam_type=Exam.objects.get(id=int(request.data['exam_type']))).exists():
            messages.success(request, 'This student already gave the selected exam.')
            data = {'exam_type': Exam.objects.all()}
            return render(request, 'exam_details.html', data)
        else:
            li = request.data['experiments'].replace(' ','')
            dam = li.split(',')
            exp = [int(x) for x in dam if len(x)>0]

            a = GivenExam.objects.create(
                                college=profile.college,
                                exam_type=Exam.objects.get(id=int(request.data['exam_type'])),
                                student=request.user,
                                exam_date=request.data['exam_date'],
                                experiments=request.data['experiments'],
                                student_roll=request.data['student_roll']
                                )
            values = Question.objects.filter(experiment__in=exp).values('id').order_by('?')[:15]

            # a list of unsaved Entry model instances
            my_list = [Answer(
                            exam_details=GivenExam.objects.get(id=a.id),
                            question=Question.objects.get(id=val['id'])
                    ) for val in values]
            Answer.objects.bulk_create(my_list)
            return redirect(f'/student/exam/{a.id}')


class ExamResult(APIView):

    def get(self, request, pk):
        exam = GivenExam.objects.get(id=pk)
        exam.exam_submitted = True
        exam.save()
        return render(request, 'result.html', {'exam_id':pk})


from django.http import FileResponse
from fpdf import FPDF, HTMLMixin
from django.core.files.base import File
import PyPDF2
import os


def some_view(request, pk):
    exam = GivenExam.objects.get(id=pk)
    student_name = exam.student.first_name+' '+exam.student.last_name
    student_roll_number = exam.student_roll
    exam_type = exam.exam_type.name
    date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
    student_name_string = exam.student.first_name + "_" + exam.student.last_name
    roll_number_string = str(exam.student_roll)
    exam_type_string = exam.exam_type.name.replace(' ','_')
    # Exam name +Student name +roll
    if exam.answer_pdf_file:
        pass
    else:
        answers = Answer.objects.filter(exam_details__id=pk)
        text = ''
        for answer in answers:
            text += "<b>Question</b> : <br>"+answer.question.text+"<br><b>Answer</b> : <br>"+answer.text+"<br><br>"
        pdf_name = exam_type_string + "_" + student_name_string + "_" + roll_number_string +'.pdf'
        class MyPdf(FPDF, HTMLMixin):
            pass
        pdf = MyPdf()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'static/font/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.write(8, "Student :"+student_name)
        # pdf.write(8, +"<br>")
        pdf.ln(8)
        pdf.write(8, "Roll number : "+student_roll_number)
        pdf.ln(8)
        pdf.write(8, "Exam type : "+exam_type)
        pdf.ln(8)
        pdf.write(8, "Date : "+date)
        pdf.ln(8)
        pdf.ln(8)
        pdf.ln(8)
        for answer in answers:
            pdf.write(8, "Question : "+answer.question.text)
            pdf.ln(8)
            # display_type = answer.question.quest_image.url.split('.')[1]

            if answer.question.question_display_type == 'video' and answer.question.quest_image != '':
                pdf.write(8, "http://13.234.122.107"+str(answer.question.quest_image.url))
                pdf.ln(8)
            elif answer.question.question_display_type == 'image' and answer.question.quest_image != '':
                pdf.image(answer.question.quest_image, h=100, w=170)
                pdf.ln(8)
            elif answer.question.quest_image == '':
                pdf.write(8, "No file")
                pdf.ln(8)
            pdf.write(8, "Answer :"+answer.text+"")
            pdf.ln(8)
            pdf.ln(8)
            pdf.ln(8)
        file_output = pdf.output(pdf_name, 'F')
        pdfFileObj = open(pdf_name, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        file_output = File(pdfFileObj)
        pageObj = pdfReader.pages[0]
        exam.answer_pdf_file.save(pdf_name, file_output)
        os.remove(pdf_name)
    return FileResponse(exam.answer_pdf_file.open(), as_attachment=True)


# showing page of exams and submitted answers details (pdf file) to staff only
class SubmittedExamDetails(APIView):
    def get(self, request):
        data = {}
        data['exam_type'] = Exam.objects.all()
        data['students'] = Profile.objects.filter(login_allow=True, college=request.user.profile.college)

        if len(request.query_params) > 0:
            exams = GivenExam.objects.filter(college=request.user.profile.college,student__profile__login_allow=True)

            if 'student' in request.query_params.keys() and request.query_params['student'] != '':
                exams = exams.filter(student__id=int(request.query_params['student']))

            if 'exam_type' in request.query_params.keys() and request.query_params['exam_type'] != '':
                exams = exams.filter(exam_type__id=request.query_params['exam_type'])
            
            if 'date' in request.query_params.keys() and request.query_params['date'] != '':
                exams = exams.filter(exam_date__date=request.query_params['date'])
                
            data['exams'] = exams
        else:
            data['exams'] = GivenExam.objects.filter(student__profile__login_allow=True, college=request.user.profile.college)
        return render(request, 'given_exam_details.html', data)

# displaying exams given by students, filtering it, deleting it
class DeleteExamDetails(APIView):
    def post(self, request, pk):
        GivenExam.objects.filter(id=pk).update(marks_scored=request.POST['marks_scored'])
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get(self, request, pk):
        GivenExam.objects.filter(id=pk).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
