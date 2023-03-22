import uuid
from entity_users.models import EntityUsers
from django.db import models
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import pandas as pd
import random,string,os
from django.core.exceptions import ValidationError
# Create your models here.

class Employee(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    company = models.ForeignKey(EntityUsers, related_name='emp_entityusers',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=225)
    middle_name = models.CharField(max_length=225,blank=True,null=True)
    last_name = models.CharField(max_length=225)
    phone_number = models.BigIntegerField(unique=True)
    email = models.CharField(unique=True,max_length=225)
    temp_password = models.CharField(max_length=225,blank=True,null=True)
    password = models.CharField(max_length=225,blank=True,null=True)
    department = models.CharField(max_length=225,blank=True,null=True)
    job_title = models.CharField(max_length=225,blank=True,null=True)
    region = models.CharField(max_length=225,blank=True,null=True)
    language = models.CharField(max_length=225,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    def clean(self):
        password1 = "".join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        temp_password = make_password(password1)
        self.temp_password = temp_password

class UploadEmployeeFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    file_name = models.FileField(upload_to='')
    company = models.ForeignKey(EntityUsers,related_name='upload_entityusers',on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "UploadEmployeeFile"

    def clean(self):
        file_name1 = str(self.file_name)
        entity_user_id = self.company.id
        path, extension = os.path.splitext(file_name1)
        if extension in [".csv", ".xlsx"]:
            try:
                if extension == '.xlsx':
                    df_group = pd.read_excel(file_name1)
                else:
                    df_group = pd.read_csv(file_name1)
                file_cloumns = set(df_group.columns)
                required_columns = {"email","phone_number"}
                if not required_columns.issubset(file_cloumns):
                    raise ValidationError("Required (email or phone_number) fields missing")
                duplicate_email = df_group.duplicated('email').sum()
                if duplicate_email > 0:
                    raise ValidationError("email should be unique")
                duplicate_phone = df_group.duplicated('phone_number').sum()
                if duplicate_phone > 0:
                    raise ValidationError("phone number should be unique")
                db_check_email = df_group["email"].to_list()
                db_check_phone = df_group["phone_number"].to_list()
                if Employee.objects.filter(Q(email__in=db_check_email) | Q(phone_number__in=db_check_phone)).exists():
                    raise ValidationError("required (email,phone_number) filed values alrady exists")
                df_group = df_group.drop_duplicates(["phone_number", "email"], keep='last', ignore_index=True)
                obj_dict = df_group.to_dict(orient='records')
                password1 = "".join(
                    random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
                temp_password = make_password(password1)
                from entity_users.models import EntityUsers
                bulk_list = []
                for obj_dic in obj_dict:
                    Employee(
                        first_name=obj_dic.get("first_name"),
                        last_name=obj_dic.get("last_name"),
                        middle_name=obj_dic.get("last_name"),
                        email=obj_dic.get("email"),
                        phone_number=obj_dic.get("phone_number"),
                        job_title=obj_dic.get("job_title"),
                        language=obj_dic.get("language"),
                        department=obj_dic.get("department"),
                        region=obj_dic.get("region"),
                        company_id=entity_user_id,
                        temp_password=temp_password

                    ).save()
            except Exception as e:
                raise ValidationError("file error due to {}".format(e))
        else:
            raise ValidationError("file format is must be csv")