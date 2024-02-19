from app import db
from sqlalchemy.orm import sessionmaker
from unidecode import unidecode
from app.models import (DATA, DOSSIER, RECHERCHE, ROLE, TAG,
                        t_A_ACCES, FICHIER, t_SOUS_DOSSIER,
                        UTILISATEUR, t_A_RECHERCHE, ATAG, 
                        t_FAVORIS, NOTIFICATION)

def get_user_by_id(id):
    return UTILISATEUR.query.filter_by(id_Utilisateur=id).first()

def get_favoris_by_user(user_id):
    return FICHIER.query.join(t_FAVORIS).filter(t_FAVORIS.c.id_Utilisateur == user_id).all()

def get_role_by_user(user_id):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    role = session.query(ROLE).join(UTILISATEUR).filter(UTILISATEUR.id_Utilisateur == user_id).first()
    session.close()
    return role

def get_dossier_by_fichier(fichier_id):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    dossier = session.query(DOSSIER).join(FICHIER).filter(FICHIER.id_Fichier == fichier_id).first()
    session.close()
    return dossier

def have_access_to_file(user_id, fichier_id):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    dossier = get_dossier_by_fichier(fichier_id)
    role = get_role_by_user(user_id)
    if dossier in role.DOSSIER_:
        session.close()
        return True
    session.close()
    return False
    

def recherche_fichier(search_term, user_id):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    search_term = unidecode(search_term.lower())
    if "&" not in search_term and "|" not in search_term and '"' not in search_term:
        search_term = search_term.split(' ')
    all_tags = []
    for term in search_term:
        tag = session.query(TAG).filter(TAG.nom_Tag == term).first()
        if tag and tag not in all_tags:
            all_tags.append(tag)
    files = {}
    for tag in all_tags:
        for file in tag.FICHIER:
            if have_access_to_file(user_id, file.id_Fichier):
                dossier = get_dossier_by_fichier(file.id_Fichier)
                if dossier not in files:
                    files[dossier] = []
                files[dossier].append(file)
    session.close()
    return files
