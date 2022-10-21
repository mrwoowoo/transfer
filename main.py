import time
from flask import Flask, redirect, render_template, request, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')

@app.route('/')
def index():
    files = []
    for file in os.scandir(app.config['UPLOAD_PATH']):
        stat = file.stat()
        timeArray = time.localtime(stat.st_ctime)
        files.append({'name': file.name, 'size': str(round(stat.st_size/1024, 2)) + 'KB', 'date': time.strftime("%Y-%m-%d %H:%M:%S", timeArray)})
    return render_template('index.html', files = files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        file.save(file_path)
        return render_template('upload.html')

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)