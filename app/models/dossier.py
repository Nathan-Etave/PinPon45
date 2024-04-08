from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.extensions import db
from app.models.sous_dossier import SOUS_DOSSIER
from app.models.fichier import FICHIER

class DOSSIER(db.Model):
    __tablename__ = 'DOSSIER'

    id_Dossier = mapped_column(Integer, primary_key=True)
    nom_Dossier = mapped_column(String(255))
    priorite_Dossier = mapped_column(Integer)
    couleur_Dossier = mapped_column(String(255))

    DOSSIER: Mapped['DOSSIER'] = relationship('DOSSIER', secondary='SOUS_DOSSIER', primaryjoin=lambda: DOSSIER.id_Dossier == SOUS_DOSSIER.c.id_Dossier_Enfant, secondaryjoin=lambda: DOSSIER.id_Dossier == SOUS_DOSSIER.c.id_Dossier_Parent, back_populates='DOSSIER_')
    DOSSIER_: Mapped['DOSSIER'] = relationship('DOSSIER', secondary='SOUS_DOSSIER', primaryjoin=lambda: DOSSIER.id_Dossier == SOUS_DOSSIER.c.id_Dossier_Parent, secondaryjoin=lambda: DOSSIER.id_Dossier == SOUS_DOSSIER.c.id_Dossier_Enfant, back_populates='DOSSIER')
    FICHIER: Mapped[List['FICHIER']] = relationship('FICHIER', uselist=True, back_populates='DOSSIER_')