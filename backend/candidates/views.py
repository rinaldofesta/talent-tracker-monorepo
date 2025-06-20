from rest_framework.decorators import api_view
from rest_framework.response import Response

#importiamo il nostro modello e il nostro serializer
from .models import Candidate
from .serializers import CandidateSerializer

@api_view(['GET'])
def get_candidates(request):
    #1. recuperare tutti gli oggetti Candidate dal database.
    candidates = Candidate.objects.all().order_by('created_at')
    
    #2. usa il serializer per tradurre la lista oggetti Python in JSON.
    serializer = CandidateSerializer(candidates, many=True)

    #3. restituisci i dati tradotti
    return Response(serializer.data)