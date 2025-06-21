# backend/Dockerfile

# Partiamo da un'immagine Python ufficiale e leggera
FROM python:3.11-slim

# Impostiamo delle variabili d'ambiente raccomandate per Python in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Impostiamo la directory di lavoro all'interno del container
WORKDIR /app

# Copiamo solo il file dei requisiti per sfruttare la cache di Docker
COPY requirements.txt /app/

# Installiamo le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo tutto il resto del codice del backend
COPY . /app/

# Il comando di default per avviare il server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]