import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app


@pytest.fixture
def client():
    # Une base SQLite en mémoire, neuve pour chaque test
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    def get_session_test():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_test
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_creer_puis_lire(client):
    r = client.post("/livres", json={"titre": "Dune", "auteur": "Frank Herbert"})
    assert r.status_code == 201
    livre = r.json()
    assert livre["statut"] == "a_lire"

    r = client.get(f"/livres/{livre['id']}")
    assert r.status_code == 200
    assert r.json()["titre"] == "Dune"


def test_note_invalide_refusee(client):
    r = client.post("/livres", json={"titre": "Dune", "auteur": "Herbert", "note": 7})
    assert r.status_code == 422


def test_filtrer_par_statut(client):
    client.post("/livres", json={"titre": "A", "auteur": "X", "statut": "lu"})
    client.post("/livres", json={"titre": "B", "auteur": "Y"})
    r = client.get("/livres", params={"statut": "lu"})
    assert [l["titre"] for l in r.json()] == ["A"]


def test_modifier_et_supprimer(client):
    id_ = client.post("/livres", json={"titre": "Dune", "auteur": "Herbert"}).json()["id"]
    r = client.patch(f"/livres/{id_}", json={"statut": "lu", "note": 5})
    assert r.json()["note"] == 5 and r.json()["titre"] == "Dune"

    assert client.delete(f"/livres/{id_}").status_code == 204
    assert client.get(f"/livres/{id_}").status_code == 404