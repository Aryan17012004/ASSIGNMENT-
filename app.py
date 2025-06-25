import os
from flask import Flask, render_template, request
from flask import redirect,flash
from flask import url_for, send_file
from werkzeug.utils import secure_filename
from model import detect_border
from model import remove_border

app = Flask(__name__)
app.secret_key = "secure_key"

INPUT_FOLDER = 'input_data'
OUTPUT_FOLDER = 'output_data'
REPORT_PATH = os.path.join(OUTPUT_FOLDER, 'border.csv')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}


os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    input_images = [f for f in os.listdir(INPUT_FOLDER) if allowed_file(f)]
    output_images = [f for f in os.listdir(OUTPUT_FOLDER) if allowed_file(f)]
    return render_template("index.html", input_images=input_images, output_images=output_images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash("No file part")
        return 

    file = request.files['image']
    if file.filename == '':
        flash("No  file")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(INPUT_FOLDER, filename)
        file.save(file_path)
        flash(" uploaded successfully")
    return redirect(url_for('index'))

@app.route('/detect')
def detect():
    detect_border.process_images(INPUT_FOLDER, REPORT_PATH)
    flash(" CSV generated.")
    return redirect(url_for('index'))

@app.route('/crop')
def crop():
    remove_border.process_images(INPUT_FOLDER, OUTPUT_FOLDER)
    flash("Cropping completed ")
    return redirect(url_for('index'))

@app.route('/download_report')
def download_report():
    return send_file(REPORT_PATH, as_attachment=True)

@app.route('/input_image/<filename>')
def input_image(filename):
    return send_file(os.path.join(INPUT_FOLDER, filename))

@app.route('/output_image/<filename>')
def output_image(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)
