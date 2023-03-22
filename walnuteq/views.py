from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password,check_password
from entity_users.models import EntityUsers
from employee.models import Employee
from django.contrib.auth.models import User
from surveyqa.models import Question
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.urls import reverse
import random, string
from walnuteq import settings
import smtplib,pathlib,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.contrib import messages

def download_sample(request):
    file_path = pathlib.Path(settings.BASE_DIR)/"sample_file/sample_file_download.csv"
    if os.path.exists(file_path):
        with open(file_path,'rb') as f:
            response = HttpResponse(f.read(),content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def validate_login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")
        entity_user = EntityUsers.objects.filter(email=email).first()
        # user = User.objects.filter(email=email).first()
        # if user and check_password(password,user.password) and user.is_superuser :
        #     user = authenticate(username=user.username,password=password)
        #     login(request,user)
        #     return HttpResponseRedirect(reverse('admin:index'))
        if entity_user:
            request.session["email"] = email
            request.session["parent_user"] = str(entity_user.parent_entityuser_id) if entity_user.parent_entityuser else None
            password = check_password(password, entity_user.temp_password)
            if password:
                company = entity_user.company.id
                question_obj = Question.objects.filter(company_id=company)
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
                return render(request, 'home.html', {"question_obj1": question_obj1})
            else:
                messages.error(request, "invalid credentails")
                return redirect("validate")
        elif Employee.objects.filter(email=email,password=password).exists():
            return None
        else:
            messages.error(request,"invalid credentails")
            return redirect("validate")
            # messages.error(request,"invalid email and password")
            # return redirect('login_users',context={"msg":messages})
    else:
        return render(request, "login.html")

def log_out_user(request):
    if request.session.get("email"):
        del request.session["email"]
        print(request.session.get("email"))
        return redirect('validate')
    else:
        return redirect('validate')

# def login_decator(func):
#     def warper(*args,**kwargs):
#         print(*args,**kwargs)

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        entity_user = EntityUsers.objects.filter(email=email).first()
        password1 = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        if user:
            final_user = user
            final_user.temp_password = user.set_password(password1)
            final_user.save()
        elif entity_user:
            final_user = entity_user
            final_user.temp_password = make_password(password1)
            final_user.save()
        else:
            final_user = None
        if final_user:
            sender_email = settings.EMAIL_HOST_USER
            password = settings.EMAIL_HOST_PASSWORD
            receiver_email = final_user.email

            message = MIMEMultipart()

            message["From"] = sender_email
            message['To'] = receiver_email
            message['Subject'] = "updated_password"
            # dic = {"first_name": [user.first_name], "last_name": [user.last_name]}
            # df = pd.DataFrame(dic)
            # file_name = f"{instance.id}.csv"
            # df.to_csv(file_name)
            # attachment = open(file_name, 'rb')
            #
            # obj = MIMEBase('application', 'octet-stream')
            #
            # obj.set_payload((attachment).read())
            # encoders.encode_base64(obj)
            # obj.add_header('Content-Disposition', "attachment; filename= " + file_name)
            message.attach(MIMEText(
                  f"updated_password: {password1}" + "\n" + f"login url: {settings.LOGIN_URL}"))
            # message.attach(obj)

            my_message = message.as_string()
            email_session = smtplib.SMTP(settings.EAMIL_HOST, settings.EMAIL_PORT)
            email_session.starttls()
            email_session.login(sender_email, password)

            email_session.sendmail(sender_email, receiver_email, my_message)
            email_session.quit()
            print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")
            return redirect("forgot_password")
        else:
            return redirect("forgot_password")
    else:
        return render(request,"forget_password.html")
