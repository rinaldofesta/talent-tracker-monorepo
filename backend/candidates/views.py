from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Candidate
from .serializers import CandidateSerializer

@api_view(['GET', 'POST'])
def candidates_list_create_view(request):
    """
    Una view che gestisce sia la visualizzazione della lista di candidati (GET)
    sia la creazione di un nuovo candidato (POST).
    """
    if request.method == 'GET':
        candidates = Candidate.objects.all().order_by('-created_at')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Passiamo i dati in arrivo dalla richiesta al serializer
        serializer = CandidateSerializer(data=request.data)
        # is_valid() controlla se i dati sono corretti secondo il nostro modello.
        # raise_exception=True restituisce automaticamente un errore 400 se non lo sono.
        serializer.is_valid(raise_exception=True)
        # Se la validazione ha successo, .save() crea il nuovo oggetto nel database.
        serializer.save()
        
        # Restituiamo i dati dell'oggetto appena creato e uno stato 201 CREATED.
        return Response(serializer.data, status=status.HTTP_201_CREATED)