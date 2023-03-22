from django.contrib import admin
from .models import UploadQAfile,DefaultQuestion,Question
# Register your models here.


class DefaultQuestionAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_add_permission(self, request):
        return False

class UploadAQfileAdmin(admin.ModelAdmin):
    list_display = ['upload_on']

    def upload_on(self,obj):
        if obj:
            try:
                if obj.upload_on:
                    return obj.upload_on
                else:
                    return None
            except:
                return obj.upload_on

admin.site.register(UploadQAfile,UploadAQfileAdmin)
admin.site.register(DefaultQuestion,DefaultQuestionAdmin)

