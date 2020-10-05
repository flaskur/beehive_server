from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
	values = {
		'message': 'some message',
		'name': 'bob',
		'age': 23,
		'cool': True
	}
	
	return jsonify(values)

@app.route('/check', methods=['POST'])
@cross_origin()
def postCheck():
	data = request.json # originally passed in as a json string, but converted to json obj

	print(data) # should be a json object?

	return jsonify(data)

@app.route('/search', methods=['POST'])
@cross_origin()
def postSearch():
	data = request.json # from request body

	print(data)

	# invoke all scrape util funcs concurrently?

	response = {
		'random': [1,2,3]
	}

	return jsonify(response)


if __name__ == '__main__':
	app.run(host='localhost', port=5000)