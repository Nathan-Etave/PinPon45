from app.search import bp
from flask_login import login_required, current_user
from flask import render_template, request
from app.extensions import db
from app.models.dossier import DOSSIER
from app.utils import Whoosh

@bp.route('/', methods=['GET', 'POST'])
@login_required
def search():
    query = request.args.get('query')
    whoosh = Whoosh()
    results = whoosh.search(query)
    results = create_rendered_list(results)
    return render_template("search/index.html", is_authenticated=True, is_admin=current_user.id_Role == 1, folders=results, query=query)

def create_rendered_list(results):
    folders = db.session.query(DOSSIER).order_by(DOSSIER.priorite_Dossier).all()
    folders_root = [folder for folder in folders if folder.DOSSIER == []]
    rendered_list = []
    for folder in folders_root:
        files = [result for result in results if result['path'].startswith(str(folder.id_Dossier))]
        subfolder = recursive_subfolder(folder, results)
        rendered_list.append({'name': folder.nom_Dossier, 'files': files, 'color': folder.couleur_Dossier, 'id': folder.id_Dossier, 'subfolder': subfolder})
    return rendered_list

def recursive_subfolder(folder, files):
    sub = []
    for subfolder in folder.DOSSIER_:
        files_sub = [result for result in files if result['path'].startswith(str(subfolder.id_Dossier))]
        sub.append({'name': subfolder.nom_Dossier, 'files': files_sub, 'color': subfolder.couleur_Dossier, 'id': subfolder.id_Dossier, 'subfolder': recursive_subfolder(subfolder, files)})
    return sub