from django.urls import path
from django.views.generic import TemplateView
from employee.views import (empviewset,
                            uploadfile,
                            empeditviewset,
                            delete_emp)

app_name = "employees"
urlpatterns = [
    path('upload_files/',TemplateView.as_view(template_name='upload-data.html'),name='upload_files'),
    path('view_employee/',empviewset,name='view_employee'),
    path('edit_employee/<pk>',empeditviewset,name='edit_employee'),
    path('delete_employee/<pk>',delete_emp,name='delete_employee'),
    path('file_data/',uploadfile,name='file_data')
]