#!/usr/bin/env python3
from flask import Flask, render_template, session, redirect, request, Response
import flask
from flask_login import LoginManager, UserMixin
import json2, os
from dotted.collection import DottedCollection, DottedDict, DottedList
from pathlib import Path
from utils.directory import directory as Dir
from utils.config import Config
from utils.auth import LoginForm

from flask_htpasswd import HtPasswdAuth

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

app.config['FLASK_HTPASSWD_PATH'] = Path(Path.cwd(),'.htppp').as_posix()
app.config['FLASK_AUTH_ALL']=True
htpasswd = HtPasswdAuth(app)

CFG = Config('config.json')

directories_dict = {}

#   # Auth
#   login_manager = LoginManager()
#   
#   login_manager.init_app(app)
#   
#   @login_manager.user_loader
#   def load_user(user_id):
#       return User.get(user_id)
#   
#   @app.route('/login', methods=['GET', 'POST'])
#   def login():
#       # Here we use a class of some kind to represent and validate our
#       # client-side form data. For example, WTForms is a library that will
#       # handle this for us, and we use a custom LoginForm to validate.
#       form = LoginForm()
#       if form.validate_on_submit():
#           # Login and validate the user.
#           # user should be an instance of your `User` class
#           login_user(user)
#   
#           flask.flash('Logged in successfully.')
#   
#           next = flask.request.args.get('next')
#           # is_safe_url should check if the url is safe for redirects.
#           # See http://flask.pocoo.org/snippets/62/ for an example.
#           if not is_safe_url(next):
#               return flask.abort(400)
#   
#           return flask.redirect(next or flask.url_for('index'))
#       return render_template('login.html', form=form)
#   
#   #End Auth

@app.route('/test/<var>', methods=['GET','POST'])
def test_url(var):
    return f"hello {var}"

@app.route('/', methods=['GET', 'POST'])
def show_folder():
    folder = request.args.get('folder')

    if folder:
        root = Path(folder)
        if not Path(CFG.get.photos.root) in root.parents:
            root = Path(CFG.get.photos.root) 
    else:
        root = Path(CFG.get.photos.root)

    curdir = Dir(root, CFG)

    curdir.generate_thumbs()

    if not curdir.path in directories_dict:
        directories_dict[curdir.path] = curdir
    
    return render_template('directory_view.html',
                            dir = curdir,
                            folder_icon = CFG.get.album.folder_icon)

@app.route('/show_photo', methods=['GET'])
def show_photo():
    photo_path = Path(request.args.get('photo'))

    if photo_path.parent in directories_dict:

        cur_dir = directories_dict[photo_path.parent]

        current_folder = cur_dir.path

        prev_path, next_path = cur_dir.image_neighbours(photo_path)

    else:
        current_folder = Path('/')
        prev_path = Path('/static/images/not_found.jpg')
        next_path =  Path('/static/images/not_found.jpg')
    print(directories_dict)

    return render_template('photo_view.html',
                            folder = current_folder.as_posix(),
                            image_path = photo_path.as_posix(),
                            prev_photo = prev_path.as_posix(),
                            next_photo = next_path.as_posix())


if __name__ == '__main__':
    print(f'PID: {os.getpid()}')
    app.run(host=CFG.get.server.ip, port=CFG.get.server.port, debug=False)
