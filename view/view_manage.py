from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from model import *
from flask_mongoengine import Pagination
import os
view_manage = Blueprint('view_manage', __name__)

@view_manage.route("/manage/<int:page>")
def manage(page):
    try:
        pag = Pagination(FileAudio.objects().order_by("-timestamp"), page, 7)
    except:
        pag = Pagination(FileAudio.objects().order_by("-timestamp"), page-1, 7)
    return render_template("manage.html", file_audios = pag)

@view_manage.route("/rename_file", methods=["POST"])
def rename_file():
    id_audio = request.form['id_audio']
    file_audio = FileAudio.objects.get(id_audio=id_audio)
    filename = request.form['file_name']
    page = request.args.get('page')
    if file_audio != None and FileAudio.objects(filename=filename).count() == 0:
        end_file = file_audio.filename[-4:]
        if not filename.endswith(end_file):
            filename = filename + end_file
        path_file = file_audio.path_file.replace(file_audio.filename, filename)
        if os.path.exists(file_audio.path_file):
            os.rename(file_audio.path_file, path_file)
        FileAudio.objects(id_audio=id_audio).update(filename=filename, path_file=path_file)
        return redirect(url_for('.manage', page=page))    
    return redirect(url_for('.manage', page=page))    

@view_manage.route("/delete_file")
def delete_file():
    id_audio = request.args.get("id_audio")
    page = request.args.get("page")
    if page==None:
        page=1
    file_audio = FileAudio.objects(id_audio=id_audio).first()
    FileAudio.objects(id_audio=id_audio).delete()
    if file_audio != None:
        if os.path.exists(file_audio.path_file):
            os.remove(file_audio.path_file)
    return redirect(url_for('view_manage.manage', page=page))
