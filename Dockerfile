# obraz do wdrożenia na Cloud Run (interfejs Streamlit)
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# kod + gotowy indeks (fragmenty.json, embeddingi.json), PDF nie jest potrzebny
COPY *.py fragmenty.json embeddingi.json ./

# Cloud Run podaje port w zmiennej PORT (domyślnie 8080)
ENV PORT=8080
# exec: streamlit dostaje sygnał zatrzymania od Cloud Run, a sh tylko podstawia $PORT
CMD ["sh", "-c", "exec streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"]
