from flask import Flask, render_template, request, jsonify, send_file
import os
import time
from docx import Document
import re
from docx.shared import Pt


from flask.helpers import url_for
from werkzeug.utils import redirect
UPLOAD = './static/files'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'
# Tạo biến lưu dữ liệu thay vì sử dụng database hay từ điển
data = {}
data['path_file'] = "" # đường dẫn file upload
data['lyrics'] = [] # đoạn văn dự đoán 
data['path_file_record'] = "" # đường dẫn file ghi âm
data['lyrics_record'] = [] # đoạn văn dự đoán từ file ghi âm


@app.route('/api/detect_upload', methods=["POST"])
def api_detect_upload():
    """
    Lưu file upload
    """
    res = {}
    file = request.files['songImport']
    file.stream.seek(0)
    path_file = os.path.join(UPLOAD, file.filename)
    file.save(path_file)
    create_at = str(time.time())
    lyrics = ['[0.0,10.97]cám ơn đoàn chủ tọa cơ hội chúng tôi xin phép trao đổi lại với đại biểu trần quang chiều cái vấn đề thứ nhất ý thì trong cái bài phát biểu tôi chỉ đề cập', '[11.4,13.27]là thống nhất với báo cáo của chính phủ', '[13.73,15.66]về cái việc mà chúng ta đang giảm', '[16.26,19.8]cái việc tăng lệ thuộc về dầu thô khoáng sản',\
         '[20.03,24.02]tuy nhiên cũng qua đây thì cũng báo cáo lại quốc hội với chính phủ', \
             '[24.32,28.01]trong cái báo cáo của chính phủ cũng nên có thêm những cái chỉ tiêu', \
                 '[28.17,30.47]các đại biểu nhìn nhận cho nó phù hợp hơn']
    res['path_file'] = path_file
    res['lyrics'] = lyrics
    res['success'] = "True"
    return jsonify(res), 200

@app.route('/detect_upload', methods=["POST", "GET"])
def detect_upload():
    """
    Lưu file upload
    """
    global data
    file = request.files['songImport']
    file.stream.seek(0)
    path_file = os.path.join(UPLOAD, file.filename)
    file.save(path_file)
    time.sleep(0.2)
    lyrics = ['[0.0,10.97]cám ơn đoàn chủ tọa cơ hội chúng tôi xin phép trao đổi lại với đại biểu trần quang chiều cái vấn đề thứ nhất ý thì trong cái bài phát biểu tôi chỉ đề cập', '[11.4,13.27]là thống nhất với báo cáo của chính phủ', '[13.73,15.66]về cái việc mà chúng ta đang giảm', '[16.26,19.8]cái việc tăng lệ thuộc về dầu thô khoáng sản',\
         '[20.03,24.02]tuy nhiên cũng qua đây thì cũng báo cáo lại quốc hội với chính phủ', \
             '[24.32,28.01]trong cái báo cáo của chính phủ cũng nên có thêm những cái chỉ tiêu', \
                 '[28.17,30.47]các đại biểu nhìn nhận cho nó phù hợp hơn']
    data['path_file'] = path_file
    data['lyrics'] = lyrics
    return redirect(url_for('homepage', remember='POST'))

@app.route("/detect_record", methods=['GET'])
def detect_record():
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

@app.route("/upload_record", methods=['POST'])
def upload_record():
    """
    Lưu file ghi âm 
    """
    global data
    if request.method == "POST":
        file = request.files['audio_data']
        file.stream.seek(0)
        path_file_record = os.path.join(UPLOAD, file.filename)
        file.save(path_file_record)
        data['path_file_record'] = path_file_record
        print(path_file_record)
        return jsonify({'success': 'True'}), 200

@app.route('/', methods=['GET', 'POST'])
def homepage():
    remember = request.args.get('remember')
    if remember != "POST":
        return render_template('home.html', file_audio="", lyrics=[])
    else:
        path_file = data['path_file']
        lyrics  = data['lyrics']
        return render_template('home.html', file_audio=path_file, lyrics=lyrics)

@app.route('/tab', methods=['GET', "POST"])
def tabpage():
    remember = request.args.get('remember')
    if remember != "POST":
        return render_template('tab.html', file_audio="", lyrics=[])
    else:
        path_file_record = data['path_file_record']
        lyrics_record  = data['lyrics_record']
        return render_template('tab.html', file_audio=path_file_record, lyrics=lyrics_record)

@app.route('/save_edit', methods=['GET'])
def save_edit():
    classify = request.args.get('classify')
    if classify == 'upload':
        return redirect(url_for('homepage', remember='POST'))
    else:
        return redirect(url_for('tabpage', remember='POST'))

@app.route('/edit_lyrics', methods=['POST'])
def edit_lyrics():
    global data
    # print(request.json)
    classify = request.args.get('classify')
    lyrics  = request.json['lyrics']
    if classify == 'upload':
        lyrics  = request.json['lyrics']
        data['lyrics'] = lyrics
    else:
        data['lyrics_record'] = lyrics
    return jsonify({"success": "ok"}), 200   


@app.route('/edit', methods=['GET'])
def editpage():
    classify = request.args.get('classify')
    if classify == 'upload':
        file_audio = request.args.get("file_audio")
        return render_template('edit.html', lyrics=data['lyrics'], file_audio=file_audio, classify=classify)
    else:
        file_audio = request.args.get("file_audio")
        return render_template('edit.html', lyrics=data['lyrics_record'], file_audio=file_audio, classify=classify)

@app.route('/export-files')
def return_files():
    classify = request.args.get('classify')
    if classify == 'upload':
        res = []
        file_name = data['path_file'].split('/')[-1]
        for line in data['lyrics']:
            res.append(line.split(']')[-1])
        path_txt = data['path_file'][:-3] + 'txt'
        with open(path_txt, 'w', encoding='utf-8') as output:
            output.write(', '.join(res))
        return send_file(path_txt, attachment_filename= file_name[:-3] + 'txt', as_attachment=True)
    else:
        res = []
        file_name = data['path_file_record'].split('/')[-1]
        for line in data['lyrics_record']:
            res.append(line.split(']')[-1])
        path_txt = data['path_file_record'][:-3] + 'txt'
        with open(path_txt, 'w', encoding='utf-8') as output:
            output.write(', '.join(res))
        return send_file(path_txt, attachment_filename= file_name[:-3] + 'txt', as_attachment=True)

@app.route('/export-doc')
def return_files_docx():
    # https://192.168.1.4:8080/export-doc?classify=upload
    classify = request.args.get('classify')
    if classify == 'upload':
        res = []
        file_name = data['path_file'].split('/')[-1]
        for line in data['lyrics']:
            res.append(line.split(']')[-1])
        path_txt = data['path_file'][:-3] + 'docx'
        document = Document()
        # document.add_heading(file_name, 0).add_run()
        myfile = ', '.join(res)
        # myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile)
        # print(myfile)
        run = document.add_paragraph().add_run(myfile)
        font = run.font
        font.name = 'Times New Roman'
        font.size = Pt(14)
        # document.add_paragraph(myfile)
        document.save(path_txt)
        return send_file(path_txt, attachment_filename= file_name[:-3] + 'docx', as_attachment=True)
    else:
        res = []
        file_name = data['path_file_record'].split('/')[-1]
        for line in data['lyrics_record']:
            res.append(line.split(']')[-1])
        path_txt = data['path_file_record'][:-3] + 'docx'
        document = Document()
        # document.add_heading(file_name, 0).add_run()
        myfile = ', '.join(res)
        # myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile)
        # print(myfile)
        run = document.add_paragraph().add_run(myfile)
        font = run.font
        font.name = 'Times New Roman'
        font.size = Pt(14)
        # document.add_paragraph(myfile)
        document.save(path_txt)
        return send_file(path_txt, attachment_filename= file_name[:-3] + 'docx', as_attachment=True)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080,
                        type=int, help='port to listen on')
    parser.add_argument('--host', default='0.0.0.0',
                        type=str, help='port to listen on')
    args = parser.parse_args()
    host = args.host
    port = args.port
    app.run(host=host, port=port, debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
