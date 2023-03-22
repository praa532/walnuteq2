from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password,check_password
from entity_users.models import EntityUsers
from django.core.mail import send_mail,EmailMessage
from walnuteq import settings
import random,string,csv
from io import StringIO
import logging

# @receiver(pre_save,sender=EntityUsers)
# def generate_passsword_send_mail(sender,instance = None,create=False,*args,**kwargs):
#     try:
#         password = "".join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k=6))
#         instance.temp_password = make_password(password)
#         email = instance.email
#         subject = "Login Credentials"
#         message = "password {} username {}".format(password,email)
#         csvfile = StringIO()
#         csvwriter = csv.writer(csvfile)
#         logging.info("sucessfully")
#         csvwriter.writerow([instance.job_titel,instance.first_name,instance.last_name,instance.phone_number])
#         msg = EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,
#                            to=[email])
#         print(csvfile.getvalue())
#         msg.attach("{}.csv".format(instance.pk),csvfile.getvalue(),"text/csv")
#         msg.send()
#     except Exception as e:
#         logging.info(e)

#     else:
#         password = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
#         instance.temp_password = make_password(password)
#         email = instance.email
#         subject = "Login Credentials"
#         message = "password {} username {}".format(password, email)
#         csvfile = StringIO()
#         csvwriter = csv.writer(csvfile)
#         logging.info("sucessfully")
#         csvwriter.writerow([instance.job_titel, instance.first_name, instance.last_name, instance.phone_number])
#         msg = EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER,
#                            to=(email,))
#         msg.attach("{}.csv".format(instance.pk), "text/csv", csvfile.getvalue())
#         msg.send()
