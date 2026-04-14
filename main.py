from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permette all'app di leggere i dati senza blocchi di sicurezza
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Questa è la nostra "bacheca": dove salviamo l'ultimo risultato ricevuto
# All'inizio mettiamo dei dati di esempio
database_temporaneo = {
    "status": "In attesa",
    "messaggio": "Il PC non ha ancora inviato dati."
}

# La tua password segreta per proteggere l'invio dei dati
SECRET_TOKEN = "Password"

@app.get("/")
def home():
    return {"message": "Server attivo. In attesa di dati..."}

# ENDPOINT PER L'APP: che chiamerà questo in GET
@app.get("/dati-aggiornati")
async def get_data():
    return database_temporaneo

# ENDPOINT PER IL TUO PC: Tu chiamerai questo in POST
@app.post("/update")
async def update_data(payload: dict, x_auth_token: str = Header(None)):
    global database_temporaneo
    
    # Controllo se la password è corretta
    if x_auth_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token non valido")
    
    # Aggiorna la bacheca con i nuovi dati
    database_temporaneo = payload
    return {"status": "successo", "message": "Dati ricevuti correttamente"}