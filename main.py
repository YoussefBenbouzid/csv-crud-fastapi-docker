#Importo librerie
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List
import csv
import uvicorn

app = FastAPI() #Istanzio applicazione FastAPI
file_csv = 'file.csv' #Creo variabile che contiene il nome del file CSV

#Imposto il modello dei dati del file CSV usando Pydantic
class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str

#Funzione per aggiungere un nuovo record nel file CSV
def aggiungiRecord(item: Item):
    with open(file_csv, mode='a', newline="") as file: #Apro il file CSV in modalità "a" ("append")
        writer = csv.writer(file) #Creo oggetto writer per scrivere sul file CSV
        writer.writerow([item.id, item.nome, item.cognome, item.codice_fiscale]) #Aggiungo una singola riga al file CSV usando l'oggetto writer e il metodo writerow
    
#Funzione che restituisce i record del file CSV come lista di oggetti Item
def recuperaRecordTutti():
    lista = [] #Creo lista vuota
    with open(file_csv, mode='r', newline="") as file: #Apro il file CSV in modalità "r" ("read")
        reader = csv.DictReader(file) #Creo oggetto reader che restituisce i record come dizionari, dei quali ogni campo è una chiave
        #Per ogni riga del file CSV aggiungo alla lista un oggetto Item
        for row in reader:
            lista.append(Item(
                id=int(row['id']),
                nome=row['nome'],
                cognome=row['cognome'],
                codice_fiscale=row['codice_fiscale']
            ))
    return lista #Restituisco la lista

#Funzione che restituisce un record del file CSV  
def recuperaRecordUno(id: int): #Segnalo che restituisco un item
    trovato = False #Flag per verificare se l'id ricercato è stato trovato
    with open(file_csv, mode='r', newline="") as file: #Apro il file CSV in modalità "r" ("read")
        reader = csv.DictReader(file) #Creo oggetto reader che restituisce i record come dizionari, dei quali ogni campo è una chiave
        #Per ogni riga del file CSV verifico se l'id è simile a quello ricercato, se la condizione è vera restituisco l'item ricercato
        for row in reader:
            if int(row['id']) == id:
                trovato = True
                return Item(
                    id=int(row['id']),
                    nome=row['nome'],
                    cognome=row['cognome'],
                    codice_fiscale=row['codice_fiscale']
                )
            if trovato == False:
                response = {
                    "message": "Item not found"
                }
                return JSONResponse(content=response)

#Funzione che modifica un record del file CSV
def modificaRecord(id: int, nuovoItem: Item):
    trovato = False #Flag per verificare se l'id ricercato è stato trovato
    lista = [] #Creo lista vuota
    with open(file_csv, mode='r', newline="") as file: #Apro il file CSV in modalità "r" ("read")
        reader = csv.DictReader(file) #Creo un oggetto reader che restituisce i record come dizionari, dei quali ogni campo è una chiave
        #Per ogni riga del file CSV verifico se l'id è simile a quello ricercato e nel caso lo sostituisco; aggiungo tutte le righe alla lista
        for row in reader:
            if int(row['id']) == id:
                trovato = True
                row['nome'] = nuovoItem.nome
                row['cognome'] = nuovoItem.cognome
                row['codice_fiscale'] = nuovoItem.codice_fiscale
            lista.append(row)
    #Sovrascrivo il file CSV
    with open(file_csv, mode='w', newline="") as file: #Apro il file CSV in modalità "w" ("write")
        fieldnames = ['id', 'nome', 'cognome', 'codice_fiscale'] #Specifico i campi
        writer = csv.DictWriter(file, fieldnames=fieldnames) #Creo un oggetto writer che scrive nel file CSV i record come dizionari
        writer.writeheader() #Scrivo l'intestazione
        writer.writerows(lista) #Scrivo nel file CSV le righe contenute nella lista
    return trovato

#Funzione che elimina un record del file CSV
def eliminaRecord(id: int):
    trovato = False #Flag per verificare se l'id ricercato è stato trovato
    lista = [] #Creo lista vuota
    with open(file_csv, mode='r', newline="") as file: #Apro il file CSV in modalità "r" ("read")
        reader = csv.DictReader(file) #Creo oggetto reader che restituisce i record come dizionari, dei quali ogni campo è una chiave
        #Per ogni riga del file CSV verifico se l'id è diverso a quello ricercato e nel caso aggiungo la riga alla lista
        for row in reader:
            if int(row['id']) == id:
                trovato = True
            if int(row['id']) != id:
                lista.append(row)
    #Sovrascrivo il file CSV
    with open(file_csv, mode='w', newline="") as file: #Apro il file CSV in modalità "w" ("write")
        fieldnames = ['id', 'nome', 'cognome', 'codice_fiscale'] #Specifico i campi
        writer = csv.DictWriter(file, fieldnames=fieldnames) #Creo un oggetto writer che scrive nel file CSV i record come dizionari
        writer.writeheader() #Scrivo l'intestazione
        writer.writerows(lista) #Scrivo nel file CSV le righe contenute nella lista
    return trovato

#Funzione che restituisce il numero dei record del file CSV
def numeroRecord():
    count = 0 #Dichiaro variabile contatore con valore iniziale uguale a zero
    with open(file_csv, mode='r', newline="") as file: #Apro il file CSV in modalità "r" ("read")
        reader = csv.reader(file) #Creo oggetto reader per leggere il file CSV
        #Per ogni riga nel file CSV incremento il valore del contatore
        for row in reader:
            count += 1
    return count #Restuisco la variabile contatore

#Endpoint per la creazione di un nuovo record: Metodo: POST, Path: /items/
@app.post("/items/")
def aggiungiItem(item: Item):
    aggiungiRecord(item) #Richiamo funzione
    response = {
        "id": item.id,
        "nome": item.nome,
        "cognome": item.cognome,
        "codice_fiscale": item.codice_fiscale
    }
    return JSONResponse(content=response)

#Endpoint per ottenere tutti i record: Metodo: GET, Path: /items/
@app.get("/items/")
def recuperaItemTutti():
    lista = recuperaRecordTutti() #Richiamo funzione
    response = [item.dict() for item in lista]  #Converto gli oggetti Item in dizionari
    return JSONResponse(content=response)

#Endpoint per ottenere un singolo record basato sull'ID: Metodo: GET, Path: /items/{id}
@app.get("/items/{id}")
def recuperaItemUno(id: int):
    item = recuperaRecordUno(id) #Richiamo funzione
    response = {
        "id": item.id,
        "nome": item.nome,
        "cognome": item.cognome,
        "codice_fiscale": item.codice_fiscale
    }
    return JSONResponse(content=response)

#Endpoint per aggiornare un record esistente: Metodo: PUT, Path: /items/{id}
@app.put("/items/{id}")
def modificaItem(id: int, nuovoItem: Item):
    trovato = modificaRecord(id, nuovoItem) #Richiamo funzione
    if trovato == False:
        response = {
            "message": "Item not found"
        }
        return JSONResponse(content=response)
    if trovato == True:
        response = {
            "id": nuovoItem.id,
            "nome": nuovoItem.nome,
            "cognome": nuovoItem.cognome,
            "codice_fiscale": nuovoItem.codice_fiscale
        }
    return JSONResponse(content=response)

#Endpoint per eliminare un record esistente: Metodo: DELETE, Path: /items/{id}
@app.delete("/items/{id}")
def eliminaItem(id: int):
    trovato = eliminaRecord(id)
    if trovato == False:
        response = {
            "message": "Item not found"
        }
        return JSONResponse(content=response)
    if trovato == True:
        response = {
            "message": "Item deleted successfully"
        }
    return JSONResponse(content=response)

#Endpoint per ottenere il numero di righe nel CSV: Metodo: GET, Path: /items/count
@app.get("/items/count")
def numeroItem():
    count = numeroRecord() #Richiamo funzione
    response = {
        "count": count
    }
    return JSONResponse(content=response)

#Eseguo l'applicazionne con server uvicorn su porta 8000 e su tutte le interfacce di rete
uvicorn.run(app, host="0.0.0.0", port=8000)