from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_candidates(request):
    """
    una view API che restituisce una lista di candidati dummy.
    """

    dummy_candidates = [
        { 'id': 1, 'name': 'Rinaldo Festa', 'title': 'Senior Full-Stack Developer' },
        { 'id': 2, 'name': 'Mario Rossi', 'title': 'Frontend Specialist' },
        { 'id': 3, 'name': 'Giulia Bianchi', 'title': 'Backend Engineer' },
    ]

    return Response(dummy_candidates)