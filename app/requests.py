from app import db
from sqlalchemy.orm import sessionmaker
from app.models import (DATA, DOSSIER, RECHERCHE, ROLE, TAG,
                        t_A_ACCES, FICHIER, t_SOUS_DOSSIER,
                        UTILISATEUR, ARECHERCHE, ATAG, 
                        t_FAVORIS, NOTIFICATION,ARECHERCHE)
import datetime
from sqlalchemy import insert
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

def get_role():
    """ permet de récupérer les rôles

    Returns:
        List : liste des rôles
    """    
    return ROLE.query.all()

def passif_to_actif(id_utilisateur):
    """ permet de passer un utilisateur de passif à actif

    Args:
        id_utilisateur (int): id de l'utilisateur
    """    
    utilisateur = UTILISATEUR.query.filter_by(id_Utilisateur=id_utilisateur).first()
    utilisateur.est_Actif_Utilisateur = 1
    db.session.commit()
def delete_notification(id_notification):
    """ permet de supprimer une notification

    Args:
        id_notification (int): id de la notification
    """    
    notification = NOTIFICATION.query.filter_by(id_Notification=id_notification).first()
    db.session.delete(notification)
    db.session.commit()
def change_role(id_utilisateur, nom_role):
    """ permet de changer le rôle d'un utilisateur

    Args:
        id_utilisateur (int): id de l'utilisateur
        id_role (int): id du rôle
    """    
    utilisateur = UTILISATEUR.query.filter_by(id_Utilisateur=id_utilisateur).first()
    role = ROLE.query.filter_by(nom_Role=nom_role).first()
    utilisateur.id_Role = role.id_Role
    db.session.commit()

def change_password(id_utilisateur,mdp):
    """ permet de changer le mot de passe d'un utilisateur

    Args:
        id_utilisateur (int): id de l'utilisateur
        mdp (str): mot de passe
    """    
    utilisateur = UTILISATEUR.query.filter_by(id_Utilisateur=id_utilisateur).first()
    utilisateur.mdp_Utilisateur = mdp
    db.session.commit()

def ok_inscrit(id_utilisateur,nom_role,id_Notification, password):
    """ permet de passer un utilisateur de inscrit à actif

    Args:
        id_utilisateur (int): id de l'utilisateur
    """    
    passif_to_actif(id_utilisateur)
    delete_notification(id_Notification)
    change_role(id_utilisateur,nom_role)
    change_password(id_utilisateur,password)
    
def add_file(file, filename, extension, tags, id_dossier):
    data = DATA(data=file)
    db.session.add(data)
    db.session.commit()
    file = FICHIER(nom_Fichier=filename, extension_Fichier=extension, id_Dossier=id_dossier, id_Data=data.id_Data)
    db.session.add(file)
    db.session.commit()
    for tag in tags:
        if not TAG.query.filter_by(nom_Tag=tag[0]).first():
            new_tag = TAG(nom_Tag=tag[0])
            db.session.add(new_tag)
            db.session.commit()
        a_tag = ATAG(id_Fichier=file.id_Fichier, nom_Tag=tag[0], nb_Occurrence=tag[1])
        db.session.add(a_tag)
        db.session.commit()
    return file.id_Fichier

def delete_utilisateur(id_utilisateur):
    """ permet de supprimer un utilisateur

    Args:
        id_utilisateur (int): id de l'utilisateur
    """    
    utilisateur = UTILISATEUR.query.filter_by(id_Utilisateur=id_utilisateur).first()
    db.session.delete(utilisateur)
    db.session.commit()

def refus_inscrit(id_utilisateur,id_Notification):
    """ permet de refuser l'inscription d'un utilisateur

    Args:
        id_utilisateur (int): id de l'utilisateur
    """    
    delete_utilisateur(id_utilisateur)
    delete_notification(id_Notification)

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
    notification = NOTIFICATION(id_Utilisateur=id_Utilisateur, id_Fichier=id_Fichier, date_Heure_Notification=date_Heure_Notification, typeNotification=typeNotification)
    session.add(notification)
    session.commit()
    session.close()

def generate_password() :
    """Génère un mot de passe aléatoire

    Returns:
        String: le mot de passe
    """    
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))

def get_notifications_inscription_user():
    notifications = (
        db.session.query(NOTIFICATION, UTILISATEUR)
        .join(UTILISATEUR, NOTIFICATION.id_Utilisateur == UTILISATEUR.id_Utilisateur)
        .all()
    )
    return notifications

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