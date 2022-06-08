from fileinput import filename
from posixpath import split
from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from local_utils import make_unique
from model import *
from datetime import datetime
import time
import os
import config
import sys
import wave
import contextlib
import random
from pydub import AudioSegment, effects
sys.path.append('..')
#.append('..')
# from inference_audio import pre_process_online
api = Blueprint('api', __name__)

def convert_to_wav(filepath):
    print("converting...."+filepath)
#    print(filepath)
    new_name = filepath[:-4]+"_.wav"
#    print(new_name)
    wav_file = AudioSegment.from_file(file=filepath)
    wav_file = wav_file.set_frame_rate(16000)
    wav_file = wav_file.set_sample_width(2)
#    wav_file = effects.normalize(wav_file)
    wav_file = wav_file.set_channels(1)
    wav_file.export(new_name, bitrate="256", format='wav')
    print("convert end")
#    print(new_name)
    return new_name



@api.route('/api/detect_upload', methods=["POST"])
def api_detect_upload():
    """
    API nhận dạng và lưu file
    """
    time.sleep(10)
    # try:
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
#        print(path_file)
    create_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    #api detect and check spell
    lyrics = ['[0.0,10.97]cám ơn đoàn chủ tọa cơ hội chúng tôi xin phép trao đổi lại với đại biểu trần quang chiều cái vấn đề thứ nhất ý thì trong cái bài phát biểu tôi chỉ đề cập', '[11.4,13.27]là thống nhất với báo cáo của chính phủ', '[13.73,15.66]về cái việc mà chúng ta đang giảm', '[16.26,19.8]cái việc tăng lệ thuộc về dầu thô khoáng sản',\
        '[20.03,24.02]tuy nhiên cũng qua đây thì cũng báo cáo lại quốc hội với chính phủ', \
            '[24.32,28.01]trong cái báo cáo của chính phủ cũng nên có thêm những cái chỉ tiêu', \
                '[28.17,30.47]các đại biểu nhìn nhận cho nó phù hợp hơn']


    # new_name = convert_to_wav(path_file)
    # os.remove(path_file)
    # path_file = new_name

##
    # text,split_dir=pre_process_online(path_file)
    text,split_dir='cám ơn đoàn chủ tọa','/media'
    # lyrics=(text)
#        print(lyrics)


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
    spell_mistake=[]
    res['id_audio'] = id_audio
    res['spell_mistake'] = spell_mistake
    res['path_file'] = path_file
    res['lyrics'] = lyrics
    res['split_dir'] = split_dir
    # print(path_file)
    # audio_seg = AudioSegment.from_wav(path_file)
    duration = "20"
#       FileAudio(id_audio= id_audio, filename=filename, create_at = create_at, timestamp=timestamp, path_file=path_file, lyrics=lyrics, spell_mistake=spell_mistake).save()
    FileAudio(id_audio= id_audio, filename=filename, create_at = create_at, timestamp=timestamp, path_file=path_file, lyrics=lyrics, spell_mistake=spell_mistake, duration=duration).save()
    res['success'] = "True"
    return jsonify(res), 200
    # except Exception as e:
    #     return jsonify({"error": "{}".format(e)}), 400

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


@api.route('/api/record_upload', methods=["POST"])
def record_upload():
    timestamp = str(int(time.time()))
    id_audio = make_unique(timestamp)
    create_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    path_file = request.json['path_file']
    filename = path_file.split('/')[-1]
    lyrics = request.json['lyrics']
    duration = request.json['duration']
    FileAudio(id_audio= id_audio, filename=filename, create_at = create_at, timestamp=timestamp, path_file=path_file, lyrics=lyrics, spell_mistake=[], duration=str(duration)).save()
    return jsonify({"success": "True", "id_audio": id_audio}), 200


@api.route('/api/get_percent', methods=["GET"])
def get_percent():
    return {"percent": random.randint(0, 100)}