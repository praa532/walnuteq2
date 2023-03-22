from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EntityUsers
from surveyqa.models import Question
from employee.models import Employee
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
# Create your views here.
# from walnuteq.views import login_decator
# @login_required
def homeviewset(request):
    email = request.session.get("email")
    entity_user = EntityUsers.objects.get(email=email)
    # emp_data = Employee.objects.filter(company__company=entity_user.company)
    question_obj = Question.objects.filter(company=entity_user.company)
    question_obj1 = []
    if question_obj:
        question_obj = question_obj.order_by("created_at")
        for data in question_obj:
            rating_data = 0
            survey_question = data.surey_questions.all()
            if survey_question:
                count = 0
                for rating in survey_question:
                    rating_data += rating.rating
                    count += 1
                if count >= 1:
                    rating_data = round(rating_data / count, 2)
            question_obj1.append({"name": data.name, "rating": rating_data, "created_at": data.created_at})
    return render(request, "home.html", {"question_obj1": question_obj1})
# @login_required(login_url="login_users")
def clientviewset1(request):
    if request.method=="POST" and request.session.get("email"):
        entity_users = EntityUsers.objects.get(email=request.session.get("email"))
        payload = request.POST
        if payload.get("email") is None:
            messages.error(request,"email is manditory")
            return redirect('entity_users:client_user1')
        if payload.get("phone") is  None:
            messages.error(request, "phone_number is manditory")
            return redirect('entity_users:client_user1')
            # return render(request, 'add-user.html', {"msg": "phone_number is manditory"})
        if payload.get("email"):
            try:
                validate_email(payload.get("email"))
            except Exception as e:
                messages.error(request, "Enter valid email")
                return redirect('entity_users:client_user1')
            if EntityUsers.objects.filter(email=payload.get("email")).exists():
                messages.error(request, "email already exists try with new one")
                return redirect('entity_users:client_user1')
        if payload.get("phone"):
            if type(payload.get("phone")) is not str:
                messages.error(request, "phone number type error")
                return redirect('entity_users:client_user1')
            elif EntityUsers.objects.filter(phone_number=payload.get("phone")).exists():
                messages.error(request, "phone_number already exists try with new one")
                return redirect('entity_users:client_user1')
        if payload.get("company"):
            from company.models import Company
            company = Company.objects.get(company_name = payload.get("company"))
            company = company.id
        else:
            company = entity_users.company.id

        if payload.get("password") and payload.get('confirm password'):
            if payload.get("password") != payload.get("confirm password"):
                messages.error(request, "password and confirm_password not matching")
                return redirect('entity_users:client_user1')
            else:
                password = make_password(payload.get('password'))
        else:
            messages.error(request, "missing password or confirm_password")
            return redirect('entity_users:client_user1')
        parent_entityuser = False
        if request.session.get('parent_user'):
            parent_entityuser = True
        entityuser=EntityUsers()
        entityuser.first_name = payload.get("firstname")
        entityuser.middle_name = payload.get("middlename")
        entityuser.last_name = payload.get("lastname")
        entityuser.email = payload.get("email")
        entityuser.password = password
        entityuser.temp_password = password
        entityuser.phone_number = int(payload.get("phone"))
        entityuser.department = payload.get("department")
        entityuser.job_title = payload.get("job_title")
        entityuser.company_id = company
        entityuser.parent_entityuser = entity_users if parent_entityuser is False else None
        entityuser.save()
        messages.success(request, "client_data saved successfully")
        return render(request,"add-user.html")
    else:
        return render(request,"add-user.html")


def clientlistview(request):
    if request.session.get("email"):
        client_data = EntityUsers.objects.all()
        return render(request,"dispay_client_users.html",{"client_data":client_data})
    else:
        return redirect("login_users")


