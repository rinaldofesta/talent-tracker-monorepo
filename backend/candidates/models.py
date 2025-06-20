from django.db import models

class Candidate(models.Model):
    # Definiamo le scelte per il campo status
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
    ]

    # CharField è un campo di testo per stringhe di piccole-medie dimensioni.
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    # Usiamo il campo 'choices' per avere un menu a tendina nell'admin di Django.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    # DateTimeField per salvare data e ora.
    # auto_now_add=True dice a Django di impostare questo campo automaticamente solo al momento della creazione dell'oggetto.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Questa funzione definisce come l'oggetto verrà mostrato, ad esempio,
        nell'interfaccia di amministrazione. Molto utile per la leggibilità.
        """
        return self.name
