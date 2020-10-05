from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
	values = {
		'message': 'some message',
		'name': 'bob',
		'age': 23,
		'cool': True
	}
	
	return jsonify(values)

@app.route('/check', methods=['POST'])
def postCheck():
	data = request.json # originally passed in as a json string, but converted to json obj

	print(data) # should be a json object?

	return jsonify(data)

if __name__ == '__main__':
	app.run(host='localhost', port=5000)