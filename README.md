# csv-crud-fastapi-docker

## Descrizione
Il progetto permette di gestire un file CSV attraverso le operazioni CRUD (Create, Read, Update, Delete).

## Configurazione dell'environment
Viene utilizzato Anaconda, piattaforma open source che permette di creare environment indipendenti.

Attraverso Anaconda Prompt si è digitato il seguente comando, che permette di creare un environment chiamato "project" e che fa riferimento alla versione 3.12 di Python e che permette di installare nell'environment vari pacchetti, in particolare Python e PIP:

```bash
conda create --name project python=3.12
```

Il seguente comando attiva l'environment:

```bash
conda activate project
```

Le dipendenze vengono impostate con le relative versioni nel file requirements.txt (salvato nella directory del progetto) e gestito attraverso PIP:

```bash
pip install -r requirements.txt
```

Tra le varie dipendenze si cita in particolare Uvicorn, server di tipo ASGI (Asynchronous Server Gateway Interface), utilizzato per questo progetto.

## Implementazione
Viene utilizzato FastAPI, framework web di Python che permette di creare API.

I dati del file CSV includono id, nome, cognome e codice fiscale e sono stati impostati con la libreria Pydantic.