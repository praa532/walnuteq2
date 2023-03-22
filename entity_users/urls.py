from django.urls import path
from entity_users.views import homeviewset,clientviewset1
app_name = "entity_users"
urlpatterns = [
    path('client_welcome/',homeviewset,name='client_welcome'),
    path('client_user1/',clientviewset1,name='client_user1'),
]