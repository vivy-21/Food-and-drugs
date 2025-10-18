from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('uploaded_file', filename=file.filename))
    else:
        return 'Invalid file type'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return f'''
<!doctype html>
<html>
<head>
    <title>Uploaded Photo</title>
    <style>
        body {{
            margin: 0;
            background-color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        a {{
            color: white;
            margin-top: 10px;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <img src="/static/uploads/{filename}" alt="Uploaded Image">
    <a href="/">Upload another</a>
</body>
</html>
'''

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    port = int(os.environ.get('port', 10000))
    app.run(host='0.0.0.0' , port=port)
   # app.run(debug=True)