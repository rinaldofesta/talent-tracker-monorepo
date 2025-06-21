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
    
@api_view(['GET', 'PATCH', 'DELETE'])
def candidate_detail_view(request, pk):
    """
    Una view che gestisce le operazioni su un singolo candidato.
    GET: Legge i dati.
    PATCH: Aggiorna parzialmente i dati.
    DELETE: Cancella il candidato.
    """
    try:
        # troviamo il candidato nel database usando la chiave primaria (pk)
        candidate = Candidate.objects.get(pk=pk)
    except Candidate.DoesNotExist:
        # se il candidato non esiste, restituiamo un errore 404 Not Found.
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # se la richiesta è GET, restituiamo i dati di quel singolo candidato
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        # se la richiesta è PATCH, passiamo al serializer sia l'istanza che vogliamo aggiornare sia i nuovi dati parziali
        serializer = CandidateSerializer(instance=candidate, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        #restituiamo i dati aggiornati del candidato
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        # se la richiesta è DELETE, cancelliamo l'oggetto nel database.
        candidate.delete()
        # e restituiamo una risposta standard 204 No Content
        return Response(status=status.HTTP_204_NO_CONTENT)