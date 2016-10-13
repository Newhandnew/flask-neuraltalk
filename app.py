#!neuraltalk2-flask/bin/python
# from flask_cors import CORS, cross_origin			# for CORS
import os
from flask import Flask, request, jsonify, abort
import uuid
import queue
import base64
import re
from time import sleep
from random import randint
# from flask import render_template, request, redirect, url_for, send_from_directory
# from werkzeug import secure_filename


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
action_queue = queue.Queue(10)
caption_result = {}


@app.route('/')
def root():
    #return send_from_directory('index.html')
    return app.send_static_file('index.html')
# -- CORS test
# @app.route('/foo')
# @cross_origin()
# def foo():
#     return 'this is a test!'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/camera', methods=['POST'])
def camera_caption():
	base64img = request.form['base64img']
	image_data = re.sub('^data:image/.+;base64,', '', base64img)
	image = base64.b64decode(image_data)
	print("get picture successfully!")
	# print('image:', base64img)
	image_uuid = str(uuid.uuid1())
	add_queue(image_uuid, image)
	# response
	resp_data = {'uuid':image_uuid}
	resp = jsonify(resp_data)
	resp.status_code = 200
	return resp

def add_queue(img_uuid, img_data):
	if action_queue.full():
		print("Can't add to queue, queue is full!!!")
	else:
		action_queue.put({'uuid':img_uuid, 'image':img_data})
	while(action_queue.empty() == False):
		action = action_queue.get()
		uuid = action['uuid']
		image = action['image']
		result = image_caption(image)
		caption_result[uuid] = result		# push to result dictionary


def image_caption(image):
	# need to implement code
	sleep(2)
	return randint(0, 1000)
	# filename = 'some_image.png'  # I assume you have a way of picking unique filenames
	# with open(filename, 'wb') as f:
	#     f.write(image)


@app.route('/caption/<pending_id>', methods=['GET'])
def caption(pending_id):
	if pending_id in caption_result:
		data = {'caption':caption_result[pending_id]}
		resp = jsonify(data)
		return resp
	else:
		return abort(404)


if __name__ == "__main__":
    # print("flask version:", Flask.__version__)
    app.run(debug=True)
    # -- CORS test
    # CORS(app)
    # app.config['CORS_HEADERS'] = 'Content-Type'

