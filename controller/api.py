from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from local_utils import make_unique
from model import *
from datetime import datetime
import time
import os
import config

api = Blueprint('api', __name__)

@api.route('/api/detect_upload', methods=["POST"])
def api_detect_upload():
    """
    API nhận dạng và lưu file
    """
    try:
        timestamp = str(int(time.time()))
        id_audio = make_unique(timestamp)
        res = {}
        file = request.files['songImport']
        file.stream.seek(0)
        filename = file.filename
        if FileAudio.objects(filename=filename).first() != None:
            filename = make_unique(filename)
        path_file = os.path.join(config.UPLOAD, filename)
        file.save(path_file)
        create_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        #api detect and check spell
        lyrics = ['[0.0,10.97]cám ơn đoàn chủ tọa cơ hội chúng tôi xin phép trao đổi lại với đại biểu trần quang chiều cái vấn đề thứ nhất ý thì trong cái bài phát biểu tôi chỉ đề cập', '[11.4,13.27]là thống nhất với báo cáo của chính phủ', '[13.73,15.66]về cái việc mà chúng ta đang giảm', '[16.26,19.8]cái việc tăng lệ thuộc về dầu thô khoáng sản',\
            '[20.03,24.02]tuy nhiên cũng qua đây thì cũng báo cáo lại quốc hội với chính phủ', \
                '[24.32,28.01]trong cái báo cáo của chính phủ cũng nên có thêm những cái chỉ tiêu', \
                    '[28.17,30.47]các đại biểu nhìn nhận cho nó phù hợp hơn']
        spell_mistake = [
            {
                "sentence": 0,
                "start_index": 7,
                "end_index": 11,
                "originalText": "đoàn",
                "suggestion": ["tạ", "báo"],
                "confidence": 1
            },
            {
                "sentence": 1,
                "start_index": 0,
                "end_index": 8,
                "originalText": "là",
                "suggestion": ["gần", "đây là"],
                "confidence": 1
            }
        ]
        res['id_audio'] = id_audio
        res['spell_mistake'] = spell_mistake
        res['path_file'] = path_file
        res['lyrics'] = lyrics
        FileAudio(id_audio= id_audio, filename=filename, create_at = create_at, timestamp=timestamp, path_file=path_file, lyrics=lyrics, spell_mistake=spell_mistake).save()
        res['success'] = "True"
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": "{}".format(e)}), 400

@api.route('/api/detect_update', methods=["PUT"])
def api_update():
    """
    API cập nhật khi sửa đoạn văn
    """
    try:
        res = {}
        id_audio = request.json['id_audio']
        #api check spell
        lyrics = request.json['lyrics']
        spell_mistake = []
        res['id_audio'] = id_audio
        res['lyrics'] = lyrics
        res['spell_mistake'] = spell_mistake
        if FileAudio.objects(id_audio=id_audio).first() != None:
            FileAudio.objects(id_audio=id_audio).update(lyrics=lyrics, spell_mistake=spell_mistake)
        res['success'] = "True"
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": "{}".format(e)}), 400        