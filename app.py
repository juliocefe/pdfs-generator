from flask import Flask, make_response, render_template, url_for, request, flash, redirect
from weasyprint import HTML, CSS
from flask_weasyprint import render_pdf
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        import pdb; pdb.set_trace()
        # check if the post request has the file part
        data = {
            "sucursal": request.form['sucursal'],
            "promotor": request.form['promotor'],
        }
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], 'evidencia.jpg'))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'evidencia.jpg'))
            pdf = render_pdf(url_for('render_format_pdf', **data), download_filename='queOndasMen', automatic_download=False )
            return pdf

    return render_template('upload_file.html')

@app.route('/renderFormatPdf')
@app.route('/renderFormatPdf/<string:sucursal>/<string:promotor>')
def render_format_pdf(sucursal="",promotor=""):
    data = {
        "sucursal": sucursal.upper(),
        "promotor": promotor.upper()
    }
    return render_template('electrolitFormatPdf.html', **data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')