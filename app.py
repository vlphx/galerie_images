# from datetime import datetime
# import random
from os import getcwd
from os.path import join
from uuid import uuid4

from flask import Flask, session, redirect, request, render_template, url_for, send_from_directory
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = "'\x0c9&\x0c]{NKJj\\7SAN+I#($DKh"
app.config.from_file('config.json', load=json.load)

mysql = MySQL()
mysql.init_app(app)


app.config['UPLOAD_FOLDER'] = join(getcwd(), 'images_envoyees')
EXTENSIONS_AUTORISEES = ['png', 'jpg', 'jpeg']


def extension_autorisee(nom_du_fichier):
    return '.' in nom_du_fichier and \
           nom_du_fichier.rsplit('.', 1)[1].lower() in EXTENSIONS_AUTORISEES


@app.route('/')
def affiche_catalogue():
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    curseur.execute('SELECT nom_du_fichier FROM image ORDER BY date_de_mise_en_ligne DESC')
    dictionnaires_images = curseur.fetchall()
    curseur.execute('SELECT nom_du_fichier FROM image ORDER BY RAND() ')
    dictionnaires_images_random = curseur.fetchmany(9)

    curseur.close()
    connexion.close()
    return render_template('index.html', dictionnaires_images=dictionnaires_images,
                           dictionnaires_images_random=dictionnaires_images_random)


@app.route('/image')
def affiche_image():
    nom_du_fichier = request.args['nom_du_fichier']
    return send_from_directory(app.config['UPLOAD_FOLDER'], nom_du_fichier)


@app.route('/page_image')
def affiche_page_image():
    nom_du_fichier = request.args['nom_du_fichier']
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    curseur.execute('SELECT createur, date_de_mise_en_ligne, titre FROM image WHERE nom_du_fichier = %s',
                    nom_du_fichier)
    dictionnaire_image = curseur.fetchone()
    curseur.close()
    connexion.close()
    return render_template('image.html', nom_du_fichier=nom_du_fichier, createur=dictionnaire_image['createur'],
                           date_de_mise_en_ligne=dictionnaire_image['date_de_mise_en_ligne'],
                           titre=dictionnaire_image['titre'])


@app.route('/connecter', methods=['GET', 'POST'])
def connecter():
    if request.method == 'POST':
        connexion = mysql.connect()
        curseur = connexion.cursor(cursor=DictCursor)
        pseudonyme = request.form['pseudonyme']
        mot_de_passe = request.form['mot_de_passe']
        curseur.execute('SELECT pseudonyme, mot_de_passe FROM membre WHERE pseudonyme = %s', pseudonyme)
        dictionnaire_membre = curseur.fetchone()
        if dictionnaire_membre is None or check_password_hash(dictionnaire_membre['mot_de_passe'],
                                                              mot_de_passe) is False:
            return render_template('erreur_de_connexion.html')
        else:
            session['pseudonyme'] = request.form['pseudonyme']
            return redirect('/connecter')
    return render_template('connecter.html')


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nouveau_pseudonyme = request.form['pseudonyme']
        nouveau_mot_de_passe = request.form['mot_de_passe']
        connexion = mysql.connect()
        curseur = connexion.cursor()
        curseur.execute('SELECT pseudonyme, mot_de_passe FROM membre WHERE pseudonyme = %s', nouveau_pseudonyme)
        dictionnaire_membre = curseur.fetchone()
        if dictionnaire_membre is not None:
            curseur.close()
            connexion.close()
            return render_template('erreur_inscription.html')
        else:
            curseur.execute('INSERT INTO membre (pseudonyme, mot_de_passe) VALUES (%s, %s)',
                            (nouveau_pseudonyme, generate_password_hash(nouveau_mot_de_passe)))
            connexion.commit()
            return render_template('inscription_reussie.html')
    return render_template('inscription.html')


@app.route('/deconnexion')
def deconnexion():
    if 'pseudonyme' in session:
        del session['pseudonyme']
    return redirect('/')


@app.route('/ajout_image')
def affiche_formulaire_envoi_image():
    return render_template('formulaire_envoi_image.html')


@app.route('/envoie_image', methods=['POST'])
def envoie_image():
    fichier = request.files['image_importe']
    if extension_autorisee(fichier.filename):
        prefixe = uuid4().hex
        nom_de_fichier_securisee = prefixe + '_' + secure_filename(fichier.filename)
        fichier.save(join(app.config['UPLOAD_FOLDER'], nom_de_fichier_securisee))
        createur = session['pseudonyme']
        titre = request.form['titre']
        connexion = mysql.connect()
        curseur = connexion.cursor()
        curseur.execute('INSERT INTO image (nom_du_fichier, createur, titre) VALUES (%s, %s, %s)',
                        (nom_de_fichier_securisee, createur, titre))
        curseur.close()
        connexion.commit()
        connexion.close()
        return redirect(url_for('affiche_page_image', nom_du_fichier=nom_de_fichier_securisee))
    else:
        return render_template('erreur_envoi_image.html')


@app.route('/artiste')
def artiste():
    connexion = mysql.connect()
    pseudonyme = request.args['createur']
    curseur = connexion.cursor(cursor=DictCursor)
    curseur.execute('SELECT nom_du_fichier, createur FROM image WHERE createur = %s', pseudonyme)
    dictionnaires_images = curseur.fetchall()
    curseur.close()
    connexion.close()
    return render_template('artiste.html', dictionnaires_images=dictionnaires_images, createur=pseudonyme)


@app.route('/artistes')
def artistes():
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    curseur.execute('SELECT pseudonyme FROM membre ORDER BY pseudonyme ASC')
    dictionnaire_createur = curseur.fetchall()
    curseur.close()
    connexion.close()
    return render_template('liste_artistes.html', dictionnaire_createur=dictionnaire_createur)


if __name__ == "__main__":
    app.run(debug=True)
