# Używamy oficjalnego Pythona 3.11
#FROM python:3.11-slim

# Ustawiamy folder roboczy w kontenerze
#WORKDIR /app

# Kopiujemy pliki projektu
#COPY . /app

# Instalujemy zależności
#RUN pip install --no-cache-dir --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt

# Otwieramy port 8501 (domyślny dla Streamlit)
#EXPOSE 8501

# Uruchamiamy Streamlit
#CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]