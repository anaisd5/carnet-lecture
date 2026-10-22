# Carnet de lecture — API

API REST pour suivre mes lectures : livres à lire, en cours, lus, et leur note.
Python · FastAPI · SQLModel · SQLite · pytest

## Lancer

    poetry install
    poetry run uvicorn app.main:app --reload
    poetry run pytest -v

Documentation interactive : http://127.0.0.1:8000/docs

## Routes

| Verbe  | Route           | Effet                                  |
|--------|-----------------|----------------------------------------|
| GET    | /livres         | Lister (filtres ?statut=, ?auteur=)    |
| POST   | /livres         | Ajouter un livre                       |
| GET    | /livres/{id}    | Lire un livre                          |
| PATCH  | /livres/{id}    | Modifier statut, note…                 |
| DELETE | /livres/{id}    | Supprimer                              |

## Tests

    pytest -v

## Auteur

Anaïs Dubois