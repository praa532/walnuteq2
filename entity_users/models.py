import csv
import logging
import pathlib
import random
import string
import uuid
from django.db import models
from company.models import Company
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.hashers import make_password
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from walnuteq import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
ROE_CHOICE = [('Company Admin','Company Admin'),('Company Stuff','Company Stuff')]
# Create your models here.

class EntityUsers(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    company = models.ForeignKey(Company, related_name='entityusers_company',on_delete=models.CASCADE,
                                blank=True,default=None,null=True)
    parent_entityuser = models.ForeignKey("self", on_delete=models.CASCADE,
                                          related_name='parent_entityusers',blank=True,null=True,default=None)
    first_name = models.CharField(max_length=225,blank=True)
    middle_name = models.CharField(max_length=225,blank=True,null=True)
    last_name = models.CharField(max_length=225,blank=True,null=True)
    phone_number = models.BigIntegerField(unique=True)
    email = models.CharField(unique=True,max_length=225)
    temp_password = models.CharField(max_length=225,blank=True)
    password = models.CharField(max_length=225,blank=True,null=True)
    department = models.CharField(max_length=225,blank=True,null=True)
    job_title = models.CharField(max_length=225,blank=True,null=True)
    region = models.CharField(max_length=225,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_role = models.CharField(max_length=50,choices=ROE_CHOICE,default='Company Admin')

    def __str__(self):
        return str(self.company)+"  "+str(self.first_name)
    class Meta:
        verbose_name = 'Company Admin'
        verbose_name_plural = 'Company Admin'
    def clean(self):

        try:
            sender_email = settings.EMAIL_HOST_USER
            password = settings.EMAIL_HOST_PASSWORD
            email_session = smtplib.SMTP(settings.EAMIL_HOST, settings.EMAIL_PORT)
            email_session.starttls()
            email_session.login(sender_email, password)
        except Exception as e:
            raise ValidationError(f"failed due to {e}")
    # @staticmethod
def password_sendmail(sender,instance,*args,**kwargs):
    # if instance._state.adding:
    instance.access_role = 'Company Stuff' if instance.parent_entityuser else 'Company Admin'
    if instance.access_role != 'Company Stuff':
        password1 = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        make_passwords=make_password(password1)
        instance.temp_password = make_passwords
        instance.password = make_passwords
        email1 = instance.email
        sender_email = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        receiver_email = email1

        message = MIMEMultipart()

        message["From"] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "sending mail for login"
        dic = {"first_name":[instance.first_name],"last_name":[instance.last_name],"email":[instance.email],
               "phone_number":[instance.phone_number]}
        df = pd.DataFrame(dic)
        file_name = f"{instance.id}.csv"
        tempstorage_dir = pathlib.Path(settings.BASE_DIR)/"temp"
        tempstorage_dir.mkdir(parents=True, exist_ok=True)
        file_name1= tempstorage_dir/file_name
        df.to_csv(file_name1,index=False)
        attachment = open(file_name1, 'rb')

        obj = MIMEBase('application', 'octet-stream')

        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition', "attachment; filename= " + file_name)
        message.attach(MIMEText(
            f"user_name: {instance.email}"+" "+f"password: {password1}"+"\n"+f"login url: {settings.LOGIN_URL}"+"\n"+"\n"+"Uploaded Sample file"))
        message.attach(obj)

        my_message = message.as_string()
        email_session = smtplib.SMTP(settings.EAMIL_HOST, settings.EMAIL_PORT)
        email_session.starttls()
        email_session.login(sender_email, password)

        email_session.sendmail(sender_email, receiver_email, my_message)
        email_session.quit()
        print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")

pre_save.connect(password_sendmail,sender=EntityUsers)