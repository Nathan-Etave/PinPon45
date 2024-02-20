from app import db
from sqlalchemy.orm import sessionmaker
from app.models import (DATA, DOSSIER, RECHERCHE, ROLE, TAG,
                        t_A_ACCES, FICHIER, t_SOUS_DOSSIER,
                        UTILISATEUR, t_A_RECHERCHE, ATAG, 
                        t_FAVORIS, NOTIFICATION)
import random
import string
def get_user_by_id(id):
    return UTILISATEUR.query.filter_by(id_Utilisateur=id).first()

def already_exist_mail(mail):
    """
    Vérifie si un utilisateur avec l'adresse e-mail donnée existe déjà dans la base de données.

    Args:
        mail (str): L'adresse e-mail à vérifier.

    Returns:
        bool: True si l'email existe déjà, False sinon.
    """
    Session = sessionmaker(bind=db.engine)
    session = Session()
    user = session.query(UTILISATEUR).filter_by(email_Utilisateur=mail).first()
    session.close()
    return user is not None

def get_user_by_email(email):
    """
    Récupère un utilisateur en fonction de son adresse e-mail.

    Args:
        email (str): L'adresse e-mail de l'utilisateur.

    Returns:
        dict: Un dictionnaire contenant les informations de l'utilisateur.
    """
    return UTILISATEUR.query.filter_by(email_Utilisateur=email).first()

def add_user( prenom, nom, email, telephone,role, mdp,est_Actif_Utilisateur):
    """
    Ajoute un utilisateur à la base de données.

    Args:
        prenom (str): Le prénom de l'utilisateur.
        nom (str): Le nom de l'utilisateur.
        email (str): L'adresse e-mail de l'utilisateur.
        telephone (str): Le numéro de téléphone de l'utilisateur.
        role (int): L'identifiant du rôle de l'utilisateur.
        mdp (str): Le mot de passe de l'utilisateur.

    Returns:
        None
    """
    Session = sessionmaker(bind=db.engine)
    session = Session()
    id = UTILISATEUR.query.count() + 1
    user = UTILISATEUR(id_Utilisateur=id, nom_Utilisateur = nom,prenom_Utilisateur = prenom, email_Utilisateur = email, telephone_Utilisateur = telephone,
                   mdp_Utilisateur = mdp,est_Actif_Utilisateur=est_Actif_Utilisateur,id_Role = role)
    session.add(user)
    session.commit()
    session.close()

def get_files_favoris(user_id) :
    """
    Récupère les fichiers favoris d'un utilisateur.

    Args:
        user_id (int): L'identifiant de l'utilisateur.

    Returns:
        list: La liste des fichiers favoris de l'utilisateur.
    """
    Session = sessionmaker(bind=db.engine)
    session = Session()
    files = session.query(FICHIER).join(t_FAVORIS).filter(t_FAVORIS.c.id_Utilisateur == user_id).all()
    session.close()
    return files
    
def generate_password() :
    """Génère un mot de passe aléatoire

    Returns:
        String: le mot de passe
    """    
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))

def create_Notification(id_Utilisateur, id_Fichier, date_Heure_Notification,typeNotification):
    """
    Crée une notification pour un utilisateur.

    Args:
        id_Utilisateur (int): L'identifiant de l'utilisateur.
        id_Fichier (int): L'identifiant du fichier.
        date_Heure_Notification (str): La date et l'heure de la notification.
        typeNotification (str): Le type de la notification.

    Returns:
        None
    """
    Session = sessionmaker(bind=db.engine)
    session = Session()
    id = NOTIFICATION.query.count() + 1
    notification = NOTIFICATION(id_Notification=id,id_Utilisateur=id_Utilisateur, id_Fichier=id_Fichier, date_Heure_Notification=date_Heure_Notification, typeNotification=typeNotification)
    session.add(notification)
    session.commit()
    session.close()
    
def change_mdp(id,mdp):
    """
    Change le mot de passe d'un utilisateur.

    Args:
        id (int): L'identifiant de l'utilisateur.
        mdp (str): Le nouveau mot de passe.

    Returns:
        None
    """
    Session = sessionmaker(bind=db.engine)
    session = Session()
    user = session.query(UTILISATEUR).filter_by(id_Utilisateur=id).first()
    user.mdp_Utilisateur = mdp
    session.commit()
    session.close()