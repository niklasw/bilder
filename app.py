#!/usr/bin/env python3
from flask import Flask, render_template, session, redirect, request, Response
import flask
import json2, os
from pathlib import Path
from utils.directory import directory as Dir
from utils.config import Config

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

#from flask_htpasswd import HtPasswdAuth
#app.config['FLASK_HTPASSWD_PATH'] = Path(Path.cwd(),'.htppp').as_posix()
#app.config['FLASK_AUTH_ALL']=True
#htpasswd = HtPasswdAuth(app)

CFG = Config('static/config.json')

directories_dict = {}

@app.route('/test/<var>', methods=['GET','POST'])
def test_url(var):
    return f"hello {var}"

@app.route('/', methods=['GET', 'POST'])
def show_folder():
    folder = request.args.get('folder')

    if folder:
        root = Path(folder)
        if not Path(CFG.path('photos/root')) in root.parents:
            root = Path(CFG.path('photos/root'))
    else:
        root = Path(CFG.path('photos/root'))

    curdir = Dir(root, CFG)

    curdir.generate_thumbs()

    if not curdir.path in directories_dict:
        directories_dict[curdir.path] = curdir
    
    return render_template('directory_view.html',
                            dir = curdir,
                            folder_icon = CFG.path('album/folder_icon'))

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

    return render_template('photo_view.html',
                            folder = current_folder.as_posix(),
                            image_path = photo_path.as_posix(),
                            prev_photo = prev_path.as_posix(),
                            next_photo = next_path.as_posix())


if __name__ == '__main__':
    print(f'PID: {os.getpid()}')
    app.run(host=CFG.path('server/ip'), port=CFG.path('server/port'), debug=False)
