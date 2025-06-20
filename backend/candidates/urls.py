from django.urls import path
from .views import get_candidates

urlpatterns = [
    path('candidates/', get_candidates, name='get-candidates'),
]