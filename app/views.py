import base64
import os
import random
import time
from app import app, nlp, job_statuses
from flask import render_template, request, redirect, url_for, make_response, send_file, jsonify, Response, current_app
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
from app.requests import *
from app.forms import *
from app import login_manager
from threading import Thread
import uuid
from app.mail import mailInscription, mailOublie, mailRefusé
from datetime import datetime
from io import BytesIO

process_functions = {
    'pdf': nlp.process_pdf,
    'docx': nlp.process_docx,
    'xlsx': nlp.process_sheet,
    'pptx': nlp.process_presentation,
    'txt': nlp.process_txt,
}

@app.after_request
def add_cookie(response):
    if not request.cookies.get('multiview_list'):
        response.set_cookie('multiview_list', ';')
    return response

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_user_by_id(current_user.get_id()).idRole == 1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return decorated_function

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form_mdp = MdpOublieForm()
    form_login = LoginForm()
    form_mdp_oublier = MdpOublieForm()
    user = get_user_by_email(form_login.mail.data)
    form_inscription = InscriptionForm()
    if form_inscription.validate_on_submit():
        password = None
        role = None
        est_Actif_Utilisateur=0
        
        if not already_exist_mail(form_inscription.mail.data):
            add_user(form_inscription.prenom.data, form_inscription.nom.data, form_inscription.mail.data,form_inscription.telephone.data,role, password,est_Actif_Utilisateur)
            create_Notification(get_user_by_email(form_inscription.mail.data).id_Utilisateur, None, datetime.now(), "Inscription")
            # mailInscription(form_inscription.mail.data, passe)
    if form_login.validate_on_submit():
        if user:
            if check_password_hash(user.mdp_Utilisateur, form_login.mdp.data) and user.est_Actif_Utilisateur==1:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                login_user(user, remember=True)
                return redirect(url_for('home'))
    if form_mdp_oublier.validate_on_submit():
        passe= generate_password()
        password = generate_password_hash(passe).decode('utf-8')
        id_utilisateur = get_user_by_email(form_mdp_oublier.mail.data).id_Utilisateur
        change_password(id_utilisateur, password)
        mailOublie(form_mdp_oublier.mail.data, passe)
    return render_template('connexion.html', form_login=form_login, form_inscription=form_inscription, form_mdp=form_mdp)

@app.route('/notification')
def notification():
    notif_inscription = get_notifications_inscription_user()
    role=get_role()
    return render_template('notification.html', liste_notifications_inscription=notif_inscription,roles=role)


@app.route('/utilisateurAccepter', methods=['POST'])
def utilisateurAccepter():
    json = request.get_json()
    id_notif = json['id']
    role = json['role']
    userId = json['userId']
    passe= generate_password()
    password = generate_password_hash(passe).decode('utf-8')
    ok_inscrit(userId, role, id_notif, password)
    email = get_user_by_id(userId).email_Utilisateur
    mailInscription(email, passe)
    return jsonify({'status': 'ok'})

@app.route('/utilisateurRefuser', methods=['POST'])
def utilisateurRefuser():
    json = request.get_json()
    id_notif = json['id']
    userId = json['userId']
    email=get_user_by_id(userId).email_Utilisateur
    refus_inscrit(userId, id_notif)
    mailRefusé(email)
    return jsonify({'status': 'ok'})