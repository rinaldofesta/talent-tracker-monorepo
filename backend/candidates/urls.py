from django.urls import path
from .views import candidates_list_create_view

urlpatterns = [
    path('candidates/', candidates_list_create_view, name='candidates-list-create'),
]