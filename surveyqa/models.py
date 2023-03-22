from django.db import models
import uuid,os,random,string
import pandas as pd
from company.models import Company
from django.db import transaction
from django.core.exceptions import ValidationError
# Create your models here.

class DefaultQuestion(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company,related_name="company_question",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Submission(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    question = models.ForeignKey(Question,related_name='surey_questions',on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_by = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class UploadQAfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    file_name = models.FileField(upload_to='')
    upload_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "UploadQAfile"

    def __str__(self):
        return str(self.id)

    def clean(self):
        file_name1 = str(self.file_name)
        path, extension = os.path.splitext(file_name1)
        if extension in [".csv", ".xlsx"]:
            try:
                if extension == '.xlsx':
                    df_group = pd.read_excel(self.file_name)
                else:
                    df_group = pd.read_csv(self.file_name)
                file_cloumns = set(df_group.columns)
                required_columns = {"Questions"}
                if not required_columns.issubset(file_cloumns):
                    raise ValidationError("Required name fields missing")
                duplicate_name = df_group.duplicated('Questions').sum()
                if duplicate_name > 0:
                    raise ValidationError("name should be unique")
                db_check_name = df_group["Questions"].to_list()
                if DefaultQuestion.objects.filter(name__in=db_check_name).exists():
                    raise ValidationError("required name filed values already exists")
                df_group = df_group.drop_duplicates(["Questions"], keep='last', ignore_index=True)
                obj_dict = df_group.to_dict(orient='records')
                from company.models import Company
                company = Company.objects.all()
                if not company.exists():
                    raise ValidationError("required to create company first")
                company = company.filter(company_question__isnull=True)
                for obj_dic in obj_dict:
                    with transaction.atomic():
                        try:
                            DefaultQuestion.objects.get(name=obj_dic.get("Questions"))
                        except:
                            DefaultQuestion(
                                name=obj_dic.get("Questions")
                            ).save()
                        for company_name in company:
                            Question(name=obj_dic.get("Questions"),
                                     company_id = company_name.id).save()


            except Exception as e:
                raise ValidationError("file error due to {}".format(e))
        else:
            raise ValidationError("file format is must be csv")