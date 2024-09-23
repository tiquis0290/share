from flask import Flask, render_template, request, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from shutil import make_archive
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return 'No selected file'

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', f'thumbnail_{filename}')

            file.save(file_path)

    files = os.listdir(UPLOAD_FOLDER)
    file_list_html = ''.join(f'<li><a href="/download/{file}">{file}</a>{thumbnail_tag(file)}</li>' for file in files)

    return file_list_html

def thumbnail_tag(filename):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return f'<img src="/download/{filename}" alt="{filename}" height="30">'
    return ''

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/download/all')
def download_all_files():
    make_archive('uploads', 'zip', 'uploads')
    return send_file('uploads.zip', as_attachment=True)

#if __name__ == '__main__':
 #   app.run(debug=True)

app.run(host='0.0.0.0', port=80)

