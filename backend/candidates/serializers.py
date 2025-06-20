from rest_framework import serializers
from .models import Candidate 

class CandidateSerializer(serializers.ModelSerializer):
    # La classe "Meta" è obbligatoria per i ModelSerializer.
    # Contiene le istruzioni per il traduttore.
    class Meta:
        # 1. ISTRUZIONE FONDAMENTALE: "Traduci questo modello".
        model = Candidate
        
        # 2. ISTRUZIONE AGGIUNTIVA: "Includi solo questi campi nella traduzione".
        fields = ['id', 'name', 'title', 'status', 'created_at']
