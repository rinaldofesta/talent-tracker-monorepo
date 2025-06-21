from django.urls import path
from .views import candidates_list_create_view, candidate_detail_view

urlpatterns = [
    #questo percorso gestisce la lista (GET) e la creazione (POST)
    path('candidates/', candidates_list_create_view, name='candidates-list-create'),
    #questo percorso gestisce le operazioni su un singolo candidato
    path('candidates/<int:pk>/', candidate_detail_view, name='candidate-detail-update-delete'),
]