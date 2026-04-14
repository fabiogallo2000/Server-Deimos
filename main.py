import json
import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_DATI = "database.json"

# Funzione per caricare i dati all'avvio
def carica_dati():
    if os.path.exists(FILE_DATI):
        with open(FILE_DATI, "r") as f:
            return json.load(f)
    return {"status": "In attesa", "messaggio": "Nessun dato ricevuto."}

# Carichiamo i dati all'avvio del server
database_temporaneo = carica_dati()
SECRET_TOKEN = "Password"

@app.get("/dati-aggiornati")
async def get_data():
    return database_temporaneo

@app.post("/update")
async def update_data(payload: dict, x_auth_token: str = Header(None)):
    global database_temporaneo
    if x_auth_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token non valido")
    
    database_temporaneo = payload
    # SALVIAMO SU DISCO
    with open(FILE_DATI, "w") as f:
        json.dump(payload, f)
        
    return {"status": "successo"}