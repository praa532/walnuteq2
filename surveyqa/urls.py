

from django.urls import path
from surveyqa.views import questions,questionviewset,editsurveyqa,questiondelete,sendsms
app_name = "surveyqas"
urlpatterns = [
    path('add_questions/',questionviewset,name='add_questions'),
    path('edit_surveyqa/<pk>',editsurveyqa,name='edit_surveyqa'),
    path('survey_qa',questions,name='survey_qa'),
    path('deleteqa/<pk>',questiondelete,name='deleteqa'),
    path('sendsms/',sendsms,name='sendsms')
]