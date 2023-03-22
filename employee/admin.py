from django.contrib import admin
from .models import Employee,UploadEmployeeFile
from django.urls import path
from django.shortcuts import render
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('temp_password','password')
    list_display = ["first_name","last_name","email","phone_number","company","created_by"]
    list_display_links = None

    def get_company(self, obj):
        if obj:
            try:
                return obj.company.company.name
            except:
                pass

    def created_by(self, obj):
        if obj:
            try:
                return obj.company.first_name
            except:
                pass

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

class UploadEmployeeFileAdmin(admin.ModelAdmin):
    list_display = ["id","company"]
    list_display_links = None

    def get_company(self, obj):
        if obj:
            try:
                return obj.company.company.name
            except:
                pass

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(UploadEmployeeFile,UploadEmployeeFileAdmin)
