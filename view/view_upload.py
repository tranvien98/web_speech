from flask import Blueprint, config
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from model import *
import requests
import config

view_upload = Blueprint('view_upload', __name__)

@view_upload.route('/detect_upload', methods=["POST", "GET"])
def detect_upload():
    """
    Hàm nhận dạng và lưu file upload
    """
    files = {}
    for form_file_param in request.files:
        fs = request.files[form_file_param]  # type FileStorage
        files[form_file_param] = (fs.filename, fs.read())
    res = requests.post(url="{}/api/detect_upload".format(config.URL), files=files, verify=False)
    data = res.json()
    return redirect(url_for('homepage', id_audio=data['id_audio']))