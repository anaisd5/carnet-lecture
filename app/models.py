from enum import Enum

from sqlmodel import Field, SQLModel


class Statut(str, Enum):
    a_lire = "a_lire"
    en_cours = "en_cours"
    lu = "lu"


class LivreBase(SQLModel):
    titre: str = Field(min_length=1, max_length=200)
    auteur: str = Field(min_length=1, max_length=120, index=True)
    statut: Statut = Statut.a_lire
    note: int | None = Field(default=None, ge=1, le=5)


class Livre(LivreBase, table=True):
    """La table SQL."""
    id: int | None = Field(default=None, primary_key=True)


class LivreCreate(LivreBase):
    """Ce que le client envoie pour créer un livre."""


class LivrePublic(LivreBase):
    """Ce que l'API renvoie."""
    id: int


class LivreUpdate(SQLModel):
    """Modification partielle : tout est facultatif."""
    titre: str | None = Field(default=None, min_length=1, max_length=200)
    auteur: str | None = Field(default=None, min_length=1, max_length=120)
    statut: Statut | None = None
    note: int | None = Field(default=None, ge=1, le=5)