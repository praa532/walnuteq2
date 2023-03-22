from django.contrib import admin
from .models import Company
from surveyqa.models import DefaultQuestion,Question
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj,form,change)
        if obj.id and not change:
            if not Question.objects.filter(company_id=obj.id).exists():
                defaultquestion = DefaultQuestion.objects.all()
                for question in defaultquestion:
                    Question(name=question.name,company_id=obj.id).save()
admin.site.register(Company,CompanyAdmin)