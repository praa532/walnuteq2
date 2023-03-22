"""walnuteq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import validate_login,log_out_user,forgot_password,download_sample
from twilio_app.views import inbound_sms
urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout_users/',log_out_user,name='logout_admin'),
    path('forgot_password/',forgot_password,name="forgot_password"),
    path('',validate_login,name='validate'),
    path('employees/',include('employee.urls')),
    path('entity_users/',include('entity_users.urls')),
    path('surveyqas/',include('surveyqa.urls')),
    path('download_sample',download_sample,name='download_sample'),
    path('sms',inbound_sms),
]

#Configure Admin Title and Header

admin.site.site_header = "WALNUT EQ"
admin.site.site_title = "walnut eq"