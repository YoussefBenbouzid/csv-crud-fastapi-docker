# csv-crud-fastapi-docker

## Descrizione
Il progetto permette di gestire un file CSV attraverso le operazioni CRUD (Create, Read, Update, Delete).

## Configurazione dell'environment
Viene utilizzato Anaconda, piattaforma open source che permette di creare environment indipendenti.

Attraverso Anaconda Prompt si è digitato il seguente comando, che permette di creare un environment chiamato "project" e che fa riferimento alla versione 3.12 di Python e che permette di installare nell'environment vari pacchetti, in particolare Pip:

```bash
conda create --name project python=3.12
```

Il seguente comando attiva l'environment:

```bash
conda activate project
```

Le dipendenze vengono impostate con le relative versioni nel file requirements.txt (salvato nella directory del progetto) e gestito attraverso Pip:

```bash
pip install -r requirements.txt
```

## Implementazione
Viene utilizzato FastAPI, framework web di Python che permette di creare API e gestire operazioni CRUD.

I dati del file CSV includono id, nome, cognome e codice fiscale e sono stati validati attraverso la classe BaseModel della libreria Pydantic.

Per intervenire sul file CSV viene importata la libreria csv.

Tra le varie dipendenze si cita poi in particolare Uvicorn, server di tipo ASGI (Asynchronous Server Gateway Interface), utilizzato per eseguire l'applicazione.

### Funzioni

#### aggiungiRecord(item: Item)

Apre il file CSV in modalità append e vi aggiunge un nuovo record contenente i dati dell'item in ingresso.

#### recuperaRecordTutti()

Apre il file CSV in modalità read e ne copia tutti i record in una lista, che viene restituita.

#### recuperaRecordUno(id: int)
Apre il file CSV in modalità read e ne legge i record; se trova l'id in ingresso restituisce il relativo item, altrimenti restituisce un messaggio di errore.

#### modificaRecord(id: int, nuovoItem: Item)
Apre il file CSV in modalità read e controlla gli id di tutti i record; se l'id in ingresso viene trovato la funzione sostituisce i campi del relativo item con i valori del nuovo item in ingresso; tutti i record vengono poi copiati in una lista, che viene usata per sovrascrivere il file CSV. La funzione restituisce il valore di un flag che segnala se l'id è stato trovato.

#### eliminaRecord(id: int)
Apre il file CSV in modalità read e ne copia tutti i record in una lista, ad eccezione del record il cui id è quello in ingresso. La lista viene usata per sovrascrivere il file CSV. La funzione restituisce il valore di un flag che segnala se l'id è stato trovato.

#### numeroRecord()
Apre il file CSV in modalità read e ne conta il numero dei record attraverso una variabile contatore, che viene restituita.

### Endpoint

#### Endpoint per la creazione di un nuovo record:
Metodo: POST, Path: /items/

#### Endpoint per ottenere tutti i record:
Metodo: GET, Path: /items/

#### EEndpoint per ottenere un singolo record basato sull'ID:
Metodo: GET, Path: /items/{id}

#### EEndpoint per aggiornare un record esistente:
Metodo: PUT, Path: /items/{id}

#### EEndpoint per eliminare un record esistente:
Metodo: DELETE, Path: /items/{id}

#### EEndpoint per ottenere il numero di righe nel CSV:
Metodo: GET, Path: /items/count
