from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, col, select

from app.database import get_session, init_db
from app.models import Livre, LivreCreate, LivrePublic, LivreUpdate, Statut


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # crée les tables au démarrage
    yield


app = FastAPI(title="Carnet de lecture", version="1.0.0", lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
def accueil():
    return {"message": "Bienvenue dans mon carnet de lecture", "docs": "/docs"}

@app.post("/livres", response_model=LivrePublic, status_code=201)
def creer_livre(livre: LivreCreate, session: SessionDep):
    db_livre = Livre.model_validate(livre)
    session.add(db_livre)
    session.commit()
    session.refresh(db_livre)
    return db_livre

@app.get("/livres", response_model=list[LivrePublic])
def lister_livres(
    session: SessionDep,
    statut: Statut | None = None,
    auteur: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    requete = select(Livre)
    if statut:
        requete = requete.where(Livre.statut == statut)
    if auteur:
        requete = requete.where(col(Livre.auteur).ilike(f"%{auteur}%"))
    return session.exec(requete.offset(offset).limit(limit)).all()

@app.get("/livres/{livre_id}", response_model=LivrePublic)
def lire_livre(livre_id: int, session: SessionDep):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return livre

@app.patch("/livres/{livre_id}", response_model=LivrePublic)
def modifier_livre(livre_id: int, modifs: LivreUpdate, session: SessionDep):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    livre.sqlmodel_update(modifs.model_dump(exclude_unset=True))
    session.add(livre)
    session.commit()
    session.refresh(livre)
    return livre

@app.delete("/livres/{livre_id}", status_code=204)
def supprimer_livre(livre_id: int, session: SessionDep):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    session.delete(livre)
    session.commit()