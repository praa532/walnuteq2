import random,string

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, redirect
from .models import UploadEmployeeFile,Employee
from entity_users.models import EntityUsers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import os
import pandas as pd
from django.contrib import messages
from django.core.validators import validate_email
# Create your views here.
# @login_required(login_url="login_users")
def empviewset(request):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        parent_data = EntityUsers.objects.filter(parent_entityuser=entity)
        emp_data = Employee.objects.filter(company__company=entity.company)
        payload = request.GET
        if payload.get('search'):
            emp_data = emp_data.filter(
                Q(first_name__iexact=payload.get('search')) | Q(last_name__iexact=payload.get("search")))
        # if parent_data:
        #     emp_data.filter(company__parent_entityuser=parent_data).distinct()
        if emp_data:
            emp_data = emp_data.order_by("created_at")
            paginator = Paginator(emp_data, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1
            try:
                emp_data = paginator.page(page)
            except:
                emp_data = paginator.page(page)
            return render(request, 'employee.html', {"emp_data": emp_data})
        else:
            return render(request, 'employee.html', {"emp_data": emp_data})
    else:
        return render(request, 'login.html')

def empeditviewset(request,pk):
    session_email = request.session.get("email")
    if session_email:
        entity = EntityUsers.objects.get(email=session_email)
        try:
            emp_data = Employee.objects.get(pk=pk)
        except Exception as e:
            messages.error(request, f"Employee details falied to upate due to{e}")
            return render(request, "edit-employee.html")
        if request.method == "POST":
            payload = request.POST
            if payload.get("email") != emp_data.email:
                try:
                    validate_email(payload.get("email"))
                except Exception as e:
                    messages.error(request, f"This email {payload.get('email')} not a valid one")
                    return render(request, "edit-employee.html", context={'emp_data': emp_data})
                if Employee.objects.filter(email=payload.get('email')).exists():
                    messages.error(request, f"This email {payload.get('email')} is already exists")
                    return render(request, "edit-employee.html",context={'emp_data':emp_data})
            if int(payload.get("phone")) != emp_data.phone_number:
                if Employee.objects.filter(phone_number=payload.get('phone')).exists():
                    messages.error(request, f"This phone {payload.get('phone')} is already exists")
                    return render(request, "edit-employee.html",{'emp_data':emp_data})
            try:
                emp_data.first_name = payload.get('first_name', emp_data.first_name)
                emp_data.last_name = payload.get('last_name', emp_data.last_name)
                emp_data.middle_name = payload.get('middle_name', emp_data.middle_name)
                emp_data.email = payload.get('email', emp_data.email)
                emp_data.phone_number = int(payload.get('phone'))
                emp_data.job_title = payload.get("job_title")
                emp_data.language = payload.get("language")
                emp_data.department = payload.get("department")
                emp_data.region = payload.get("region")
                emp_data.save()
                messages.success(request, 'emp details updated')
                return redirect("employees:view_employee")
            except Exception as e:
                messages.error(request, f"failed to save data in db due to {e}")
                return render(request, "edit-employee.html", {'emp_data': emp_data})
        else:
            return render(request,"edit-employee.html",context={'emp_data':emp_data})

    else:
        return render(request,'login.html')

def delete_emp(request,pk):
    session_email = request.session.get("email")
    try:
        emp_data = Employee.objects.get(pk=pk)
        emp_data.delete()
        messages.success(request, 'emp details deleted')
        return redirect("employees:view_employee")
    except Exception as e:
        messages.error(request, f"Employee details falied to upate due to{e}")
        return render(request, "edit-employee.html")


# @login_required(login_url="login_users")
def uploadfile(request):
    if request.method == "POST":
        try:
            file_name = request.FILES['file']
            session_email = request.session.get("email")
            file_name1= str(file_name)
            path,extension = os.path.splitext(file_name1)
            if extension in [".csv",".xlsx"]:
                try:
                    if extension == '.xlsx':
                        df_group = pd.read_excel(file_name)
                    else:
                        df_group = pd.read_csv(file_name)
                    file_cloumns = set(df_group.columns)
                    required_columns = {"email", "phone_number"}
                    if not required_columns.issubset(file_cloumns):
                        messages.error(request,'Required (email or phone_number) fields missing')
                        return render(request,"upload-data.html")
                    duplicate_email = df_group.duplicated('email').sum()
                    if duplicate_email > 0:
                        messages.error(request,"email should be unique")
                        return render(request,"upload-data.html")
                    duplicate_phone = df_group.duplicated('phone_number').sum()
                    if duplicate_phone > 0:
                        messages.error(request,'phone number should be unique')
                        return render(request,"upload-data.html")
                    db_check_email = df_group["email"].to_list()
                    db_check_phone =  df_group["phone_number"].to_list()
                    if Employee.objects.filter(Q(email__in=db_check_email) | Q(phone_number__in=db_check_phone)).exists():
                        messages.error(request,'required (email,phone_number) filed values alrady exists')
                        return render(request,"upload-data.html")
                    df_group =df_group.drop_duplicates(["phone_number","email"],keep='last',ignore_index=True)
                    obj_dict = df_group.to_dict(orient='records')
                    password1 = "".join(
                        random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
                    temp_password = make_password(password1)
                    from entity_users.models import EntityUsers
                    entity = EntityUsers.objects.get(email=session_email)
                    bulk_list = []
                    for obj_dic in obj_dict:
                        Employee(
                                first_name = obj_dic.get("first_name"),
                                last_name = obj_dic.get("last_name"),
                                middle_name = obj_dic.get("last_name"),
                                email = obj_dic.get("email"),
                                phone_number = obj_dic.get("phone_number"),
                                job_title=obj_dic.get("job_title"),
                                language=obj_dic.get("language"),
                                department=obj_dic.get("department"),
                                region=obj_dic.get("region"),
                                company= entity,
                                temp_password = temp_password,
                                password = temp_password

                        ).save()
                        messages.success(request,'data saved.')
                    return render(request,"upload-data.html")
                except Exception as e:
                    messages.error(request,"file error due to {}".format(e))
                    return render(request,"upload-data.html")
            else:
                messages.error(request,'file format must be .csv')
                return render(request, "upload-data.html")
        except Exception as e:
            messages.error(request, f'file upload failed due to {e}')
            return render(request, "upload-data.html")
    else:
        return render(request, "upload-data.html")