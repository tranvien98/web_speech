from flask import Flask, render_template, request, jsonify, session, send_file
import os
UPLOAD = './static/files'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "GET":
        return render_template('home.html', file_audio="", lyrics=[])
    else:
        # print(request.json)
        path_file = session['path_file']
        lyrics  = session['lyrics']
        return render_template('home.html', file_audio=path_file, lyrics=lyrics)

@app.route('/edit_lyrics', methods=['GET', 'POST'])
def edit_lyrics():
    if request.method == "GET":
        return render_template('home.html', file_audio="", lyrics=[])
    else:
        # print(request.json)

        lyrics  = request.json['lyrics']
        session['lyrics'] = lyrics
        return jsonify({"success": "ok"}), 200
       

@app.route('/tab', methods=['GET'])
def tabpage():
    return render_template('tab.html')

@app.route('/edit', methods=['GET'])
def editpage():
    return render_template('edit.html', lyrics=session['lyrics'])

@app.route('/detect', methods=["POST"])
def detect():
    # print(request.files)
    file = request.files['songImport']
    file.stream.seek(0)
    path_file = os.path.join(UPLOAD, file.filename)
    # print(path_file)
    file.save(path_file)
    # gọi api dự đoán lyrics
    lyrics = ["[00:00.06]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em","[00:02.66]Ca sĩ: Phan Mạnh Quỳnh","[00:08.06]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em","[00:10.66]Ca sĩ: Phan Mạnh Quỳnh"];
    session['path_file'] = path_file
    session['lyrics'] = lyrics
    return render_template('home.html', file_audio=path_file, lyrics=lyrics)

@app.route('/export-files')
def return_files():
    res = []
    file_name = session['path_file'].split('/')[-1]
    for line in session['lyrics']:
        res.append(line[10:])
    path_txt = session['path_file'][:-3] + 'txt'
    with open(path_txt, 'w', encoding='utf-8') as output:
        output.write(' '.join(res))
    return send_file(path_txt, attachment_filename= file_name[:-3] + 'txt', as_attachment=True)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5050,
                        type=int, help='port to listen on')
    parser.add_argument('--host', default='0.0.0.0',
                        type=str, help='port to listen on')
    args = parser.parse_args()
    host = args.host
    port = args.port
    app.run(host=host, port=port, debug=True, threaded=False)