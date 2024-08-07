#Importo le librerie che mi servono
from fastapi import FastAPI
from pydantic import BaseModel
import csv
import os
import uvicorn
from typing import List

app = FastAPI() #Istanzio applicazione FastAPI
file_csv = 'file.csv' #Creo variabile che contiene il nome del file CSV

#Imposto il modello dei dati del file CSV usando Pydantic
class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str

#Funzione per aggiungere un nuovo record nel CSV
def aggiungiRecord(item: Item):
    with open(file_csv, mode='a') as file: #Apro il file CSV in modalità "a" ("append")
        writer = csv.writer(file) #Definisco oggetto per scrivere i dati nel file CSV
        writer.writerow([item.id, item.nome, item.cognome, item.codice_fiscale]) #Aggiungo una singola riga al file CSV usando l'oggetto writer e il metodo writerow
    
#Funzione che restituisce i record nel file CSV come lista di oggetti Item
def recuperaRecordTutti(): #Segnalo che restituisco una lista
    listaRecord = [] #Creo una lista vuota
    if os.path.isfile(file_csv): #Controllo se il file esiste
        with open(file_csv, mode='r') as file: #Apro il file CSV in modalità "r" ("read")
            reader = csv.DictReader(file) #Creo un lettore che restituisce i record come dizionari, dei quali ogni colonna è una chiave
            for row in reader: #Per ogni ogni riga del file CSV aggiungo alla lista un oggetto Item
                listaRecord.append(Item(
                    id=int(row['id']),
                    nome=row['nome'],
                    cognome=row['cognome'],
                    codice_fiscale=row['codice_fiscale']
                ))
    return listaRecord #Restituisco la lista

#Funzione che restituisce un record del file CSV  
def recuperaRecordUno(id: int): #Segnalo che restituisco un item
    if os.path.isfile(file_csv): #Controllo se il file CSV esiste
        with open(file_csv, mode='r') as file: #Apro il file CSV in modalità "r" ("read")
            reader = csv.DictReader(file) #Creo un lettore che restituisce i record come dizionari, dei quali ogni colonna è una chiave
            for row in reader:
                if int(row['id']) == id: #Per ogni ogni riga del file CSV verifico se l'id è simile a quello ricercato
                    return Item( #Se la condizione è vera ritorno l'item ricercato
                        id=int(row['id']),
                        nome=row['nome'],
                        cognome=row['cognome'],
                        codice_fiscale=row['codice_fiscale']
                    )

#Funzione che modifica un record del file CSV
def modificaRecord(id: int, nuovoItem: Item):
    listaRecord = []
    if os.path.isfile(file_csv): #Controllo se il file CSV esiste
        with open(file_csv, mode='r') as file: #Apro il file CSV in modalità "r" ("read")
            reader = csv.DictReader(file) #Creo un lettore che restituisce i record come dizionari, dei quali ogni colonna è una chiave
            for row in reader:
                if int(row['id']) == id: #Per ogni ogni riga del file CSV verifico se l'id è simile a quello ricercato
                    id=int(row['id']),
                    row['nome'] = nuovoItem.nome
                    row['cognome'] = nuovoItem.cognome
                    row['codice_fiscale'] = nuovoItem.codice_fiscale
                listaRecord.append(row)
        with open(file_csv, mode='w') as file:
            fieldnames = ['id', 'nome', 'cognome', 'codice_fiscale']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listaRecord)

#Funzione che elimina un record del file CSV
def eliminaRecord(id: int):
    listaRecord = []
    if os.path.isfile(file_csv): #Controllo se il file CSV esiste
        with open(file_csv, mode='r') as file: #Apro il file CSV in modalità "r" ("read")
            reader = csv.DictReader(file) #Creo un lettore che restituisce i record come dizionari, dei quali ogni colonna è una chiave
            for row in reader:
                if int(row['id'] != id):
                    listaRecord.append(row)
        with open(file_csv, mode='w') as file:
            fieldnames = ['id', 'nome', 'cognome', 'codice_fiscale']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listaRecord)

#Funzione che restituisce il numero dei record del file CSV
def numeroRecord():
    count = 0 #Dichiaro variabile contatore con valore iniziale 0
    if os.path.isfile(file_csv): #Controllo se il file esiste
        with open(file_csv, mode='r') as file:
            reader = csv.reader(file)
            for row in reader: #Per ogni riga nel file CSV incremento il valore del contatore
                count += 1
    return count #Restuisco la variabile contatore

#Endpoint per la creazione di un nuovo record: POST, Path: /items/
@app.post("/items/")
def aggiungiItem(item: Item):
    aggiungiRecord(item) #Richiamo funzione

#Endpoint per ottenere tutti i record: GET, Path: /items/
@app.get("/items/")
def recuperaItemTutti():
    listaRecord = recuperaRecordTutti() #Richiamo funzione

#Endpoint per ottenere un singolo record basato sull'ID: GET, Path: /items/{id}
@app.get("/items/{id}")
def recuperaItemUno(idRecord: int):
    record = recuperaRecordUno(idRecord) #Richiamo funzione

#Endpoint per aggiornare un record esistente: PUT, Path: /items/{id}
@app.put("/items/{id}")
def modificaItem(id: int, nuovoItem: Item):
    record = modificaRecord(id, nuovoItem) #Richiamo funzione

#Endpoint per eliminare un record esistente: DELETE, Path: /items/{id}
@app.delete("/items/{id}")
def eliminaItem(id: int):
    eliminaRecord(id)

#Endpoint per ottenere il numero di righe nel CSV: GET, Path: /items/count
@app.get("/items/count")
def numeroItem():
    count = numeroRecord() #Richiamo funzione

#Eseguo l'applicazionne con server uvicorn su porta 8000 e su tutte le interfacce di rete
uvicorn.run(app, host="0.0.0.0", port=8000)