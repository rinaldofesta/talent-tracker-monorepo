from django.contrib import admin
from .models import Candidate

#registra il modello per renderlo visibile nell'interfaccia di admin
admin.site.register(Candidate)
