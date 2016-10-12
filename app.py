#!neuraltalk2-flask/bin/python
# from flask_cors import CORS, cross_origin			# for CORS
import os
from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    #return send_from_directory('index.html')
    return app.send_static_file('index.html')
# -- CORS test
# @app.route('/foo')
# @cross_origin()
# def foo():
#     return 'this is a test!'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# base directory
basedir = os.path.abspath(os.path.dirname(__file__))
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/camera', methods=['POST'])
def camera_caption():
	base64img = request.form['base64img']
	# print('image:', base64img)
	return 'this is a test'



if __name__ == "__main__":
    # print("flask version:", Flask.__version__)
    app.run(debug=True)
    # -- CORS test
    # CORS(app)
    # app.config['CORS_HEADERS'] = 'Content-Type'

