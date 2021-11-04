from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from model import *

view_record = Blueprint('view_record', __name__)
@view_record.route("/detect_record", methods=['GET'])
def detect_record():
    """
    Hàm nhận dạng file record
    """
    global data
    path_file_record = data['path_file_record'] 
    lyrics_record = ['[0.0,10.97]cám ơn đoàn chủ tọa', \
        '[11.4,13.27]là thống nhất ', '[13.73,15.66]về cái việc mà chúng ta đang giảm', \
            '[16.26,19.8]cái việc tăng lệ thuộc về dầu thô khoáng sản',\
        '[20.03,24.02]tuy nhiên cũng qua đây', \
            '[24.32,28.01]trong cái báo cáo của chính phủ cũng nên có thêm những cái chỉ tiêu', \
                '[28.17,30.47]các đại biểu nhìn nhận cho nó phù hợp hơn']
    data['lyrics_record'] = lyrics_record
    return render_template('tab.html', file_audio=path_file_record, lyrics=lyrics_record)

@view_record.route("/upload_record", methods=['POST'])
def upload_record():
    """
    Hàm lưu file record
    """
    global data
    if request.method == "POST":
        file = request.files['audio_data']
        file.stream.seek(0)
        path_file_record = os.path.join(UPLOAD, file.filename)
        file.save(path_file_record)
        data['path_file_record'] = path_file_record
        create_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        file_save = FileAudio(filename=file.filename, create_at = create_at, path_file=path_file_record)
        db.session.add(file_save)
        db.session.commit()
        return jsonify({'success': 'True'}), 200

