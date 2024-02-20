import os
from app import app, nlp
from flask import render_template, request, redirect, url_for, make_response, send_file, jsonify, Response
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
from app.requests import *
from app.forms import *
from app import login_manager
from datetime import datetime


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

def activated_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_user_by_id(current_user.get_id()).idRole != 2:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    user = get_user_by_email(form_login.mail.data)
    form_inscription = InscriptionForm()
    print(form_inscription.validate_on_submit())
    if form_inscription.validate_on_submit():
        #une mdp aléatoire est généré
        passe= generate_password()
        password = generate_password_hash(passe).decode('utf-8')
        print(password)
        print(passe)
        
        print("Form validé")
        role = None
        est_Actif_Utilisateur=0
        
        if already_exist_mail(form_inscription.mail.data):
            print("Mail déjà utilisé")
            
        else:
            print("Mail non utilisé")
            add_user(form_inscription.prenom.data, form_inscription.nom.data, form_inscription.mail.data,form_inscription.telephone.data,role, password,est_Actif_Utilisateur)
            create_Notification(get_user_by_email(form_inscription.mail.data).id_Utilisateur, None, datetime.now(), "Inscription")
    if form_login.validate_on_submit():
        print("cc")
        if user:
            print("user")
            if check_password_hash(user.mdpPompier, form_login.mdp.data):
                print("mdp ok")
                login_user(user, remember=True)
                return redirect(url_for('home'))
    return render_template('connexion.html', form_login=form_login, form_inscription=form_inscription)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

