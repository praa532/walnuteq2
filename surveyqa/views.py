from django.shortcuts import render,redirect
from entity_users.models import EntityUsers
from twilio_app.views import validate_twilio
from company.models import Company
from surveyqa.models import Question,Submission
from employee.models import Employee
from django.core.paginator import Paginator
from django.contrib import messages
from walnuteq import settings
# Create your views here.
def questionviewset(request):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        if request.method == "POST":
            name = request.POST.get("question")
            if name:
                if Question.objects.filter(name=name,company=entity.company).exists():
                    messages.error(request,f"question already exists for this company {entity.company}")
                    return render(request,'add-questions.html')
                elif request.POST.get("question")[-1] != "?":
                    messages.error(request, f"question is meaningful format")
                    return render(request,'add-questions.html')
                else:
                    Question(name=request.POST.get("question"),
                             company=entity.company).save()
                    return redirect('surveyqas:survey_qa')
        else:
            return render(request, 'add-questions.html')
    else:
        return render(request, 'login.html')



def editsurveyqa(request,pk):
    session_email = request.session.get("email")
    if session_email:
        if request.method == "POST":
            payload = request.POST
            question_obj = Question.objects.get(id=pk)
            try:

                if payload.get("question") and question_obj.name != payload.get("question"):
                    question_obj.name = payload.get("question")
                    question_obj.save()
                    messages.success(request,"question updated")
                    return redirect('surveyqas:survey_qa')
                else:
                    return redirect('surveyqas:survey_qa')

            except Exception as e:
                messages.error(request,f"question updation failed due to {e}")
                return render(request,'edit-survey.html',context={"question_obj":question_obj})
        else:

            question_obj = Question.objects.get(id=pk)
            return  render(request,"edit-survey.html",context={"question_obj":question_obj})
    else:
        return render(request, 'login.html')

def questions(request):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        company = entity.company
        question_obj = Question.objects.filter(company=company)
        if question_obj:
            question_obj = question_obj.order_by("created_at")
            paginator = Paginator(question_obj,5)
            try:
                page = int(request.GET.get('page','1'))
            except:
                page = 1
            try:
                question_obj = paginator.page(page)
            except:
                question_obj = paginator.page(page)
            return render(request, 'survey-qa.html', {"question_obj": question_obj})
        else:
            return render(request,'survey-qa.html')
    else:
        return render(request, 'login.html')


def questiondelete(request,pk):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        company = entity.company.id
        question = Question.objects.get(id=pk,company_id=company)
        question.delete()
        messages.success(request,f'qustion deleted done')
        return redirect('surveyqas:survey_qa')

def sendsms(request):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        company = entity.company.id
        if request.method == "GET":
            question = Question.objects.filter(company_id=company)
            employee = Employee.objects.filter(company__company_id=company)
            context  = {"question_obj":question,"employee_obj":employee}
            return render(request,"quick-send.html",context=context)
        else:
            payload = request.POST
            emp_ph = payload.get("ph_no")
            que = payload.get("ques")
            if emp_ph is None or que is None:
                messages.error(request, "issue with post data")
                return redirect("surveyqas:sendsms")
            elif emp_ph is not None and not emp_ph.isdigit():
                messages.error(request, "Phone number issue")
                return redirect("surveyqas:sendsms")
            elif que is  not None and type(que) != str:
                messages.error(request, "question error")
                return redirect("surveyqas:sendsms")
            try:
                emp_obj=Employee.objects.get(phone_number=int(emp_ph))
            except Exception as e:
                emp_obj = None
                messages.error(request, f"this phone_number {emp_ph} not link with any employee")
                return redirect("surveyqas:sendsms")
            try:
                question = Question.objects.get(name=que,company_id=company)
            except Exception as e:
                question = None
                messages.error(request, f"This question {que} not link with this company {entity.company}")
                return redirect("surveyqas:sendsms")
            responseData=validate_twilio()
            if type(responseData) is bool:
                messages.error(request, "Twilio Credential issue")
                return redirect("surveyqas:sendsms")
            else:
                try:
                    message=responseData.messages.create(body=que,from_=settings.TWILIO_NUMBER,to="+19802925688")
                except Exception as e:
                    messages.error(request, f"something went wrong due to {e}")
                    return redirect("surveyqas:sendsms")

                if message.status != "failed":
                    submission_obj = Submission.objects.filter(question=question,created_by=emp_obj.id).last()
                    if submission_obj:
                        submission_obj.question = question
                        submission_obj.created_by = emp_obj.id
                        submission_obj.save()
                        messages.success(request, "Message sent successfully.")
                        return redirect("surveyqas:sendsms")
                    else:
                        submission_obj=Submission()
                        submission_obj.question = question
                        submission_obj.created_by = emp_obj.id
                        submission_obj.save()
                        messages.success(request, "Message sent successfully.")
                        return redirect("surveyqas:sendsms")
                else:
                    messages.error(request, "Message not sent something went wrong.")
                    return redirect("surveyqas:sendsms")

