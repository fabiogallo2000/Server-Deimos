import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- CONNESSIONE MONGO ---
# Prenderemo la stringa di connessione dalle impostazioni di Render per sicurezza
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["progetto_deimos"]
collection = db["risultati"]

SECRET_TOKEN = "Password" # La stessa che usi sul PC

@app.get("/dati-aggiornati")
async def get_data():
    # Cerca l'ultimo documento salvato, escludendo l'ID interno di Mongo
    doc = collection.find_one({}, {"_id": 0})
    if doc:
        return doc
    return {"status": "In attesa", "messaggio": "Nessun dato nel database."}

@app.post("/update")
async def update_data(payload: dict, x_auth_token: str = Header(None)):
    if x_auth_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token non valido")
    
    # Sovrascrive i dati esistenti (o ne crea di nuovi se non esistono)
    collection.replace_one({}, payload, upsert=True)
    return {"status": "successo"}