#!neuraltalk2-flask/bin/python
from flask import Flask
from flask_cors import CORS, cross_origin

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    #return send_from_directory('index.html')
    return app.send_static_file('index.html')

@app.route('/foo')
@cross_origin()
def foo():
    return 'this is a test!'


if __name__ == "__main__":
    # print("flask version:", Flask.__version__)
    app.run(debug=True)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

