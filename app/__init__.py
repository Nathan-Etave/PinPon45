import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_dropzone import Dropzone
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(__file__), 'database'))):
    os.makedirs(os.path.normpath(os.path.join(os.path.dirname(__file__), 'database')))
if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(__file__), 'static/temp'))):
    os.makedirs(os.path.normpath(os.path.join(os.path.dirname(__file__), 'static/temp')))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.normpath(os.path.join(os.path.dirname(__file__), 'database/app.db'))
# app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
# app.config['DROPZONE_DEFAULT_MESSAGE'] = ''
# app.config['DROPZONE_MAX_FILE_SIZE'] = 2048
# app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
# app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pdf, .docx, .xlsx, .pptx, .txt, .jpg, .jpeg, .png, .gif'
app.config['UPLOADED_TEMP_DEST'] = os.path.normpath(os.path.join(os.path.dirname(__file__), 'static/temp'))
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db = SQLAlchemy(app)
# dropzone = Dropzone(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'connexion'
job_statuses = {}
toolbar = DebugToolbarExtension(app)

from app import views
from app import models
from app import database
from app import requests
from app import forms
from app import nlp
from app import mail
