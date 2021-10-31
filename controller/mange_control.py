from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from model import *

manage_control = Blueprint('manage_control', __name__)

@manage_control.route("/manage")
def manage():
    return render_template("manage.html", file_audios = FileAudio.query.all())

@manage_control.route("/rename_file", methods=["POST"])
def rename_file():
    file_audio = FileAudio.query.get(int(request.form['file_id']))
    file_name = request.form['file_name']
    if file_audio == None:
        return redirect(url_for('.manage'))    
    file_audio.filename = file_name
    db.session.commit()
    return redirect(url_for('.manage'))    

@manage_control.route("/delete_file")
def delete_file():
    file_id = request.args.get("file_id")
    file_audio = FileAudio.query.get(int(file_id))
    if file_audio == None:
        return render_template("manage.html", file_audios = FileAudio.query.all())
    db.session.delete(file_audio)
    db.session.commit()
    return render_template("manage.html", file_audios = FileAudio.query.all())
