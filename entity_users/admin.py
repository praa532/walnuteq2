from django.contrib import admin
from django import forms
from .models import EntityUsers
# Register your models here.

class EntityUsersform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].required = True

    class Meta:
        model = EntityUsers
        fields = '__all__'


class EntityUsersAdmin(admin.ModelAdmin):
    form = EntityUsersform
    exclude = ('parent_entityuser', 'temp_password')
    readonly_fields = ('access_role',)
    list_display = ["first_name", "last_name", "email", "phone_number", "company", "access_role"]

    # def save_model(self, request, obj, form, change):
    #     print(obj.temp_password)
    #     obj.save()

    # def password_method(self,obj):
    #     return obj.password if obj.password else ''
    # password_method.short_description = 'Password'

    def get_exclude(self, request, obj=None):
        if not obj:
            return ('password', 'temp_password', 'parent_entityuser')
        return super().get_exclude(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('password', 'access_role')
        return super().get_readonly_fields(request, obj)

    def get_password(self, obj):
        if obj.temp_password:
            return obj.temp_password
        else:
            return obj.password


admin.site.register(EntityUsers, EntityUsersAdmin)