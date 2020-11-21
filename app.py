from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sys
sys.path.insert(0, '/util/scrape_salt.py')
sys.path.insert(0, '/util/scrape_utah.py')
sys.path.insert(0, '/util/scrape_wasatch.py')
sys.path.insert(0, '/util/scrape_redfin.py')
import util.scrape_salt as scrape_salt
import util.scrape_utah as scrape_utah
import util.scrape_wasatch as scrape_wasatch
import util.scrape_redfin as scrape_redfin

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

# set to post method later
@app.route('/scrape', methods=['POST'])
@cross_origin()
def postScrape():
	# saltZipcodes = ['84116', '84104', '84105', '84103', '84108', '84102', '84106', '84111', '84115', '84109', '84101', '84112', '84113', '84119', '84044', '84107', '84114', '84117', '84118', '84120', '84121', '84123', '84124', '84128', '84129', '84133', '84138', '84144', '84180', '84132', '84134', '84136', '84139', '84141', '84143', '84148', '84150', '84184', '84189', '84190', '84199', '84110', '84122', '84125', '84126', '84127', '84130', '84131', '84145', '84147', '84151', '84152', '84157', '84158', '84165', '84170', '84171', '84093']
	saltZipcodes = ['84006', '84020', '84096', '84044', '84047', '84065', '84101', '84102', '84103', '84104', '84105', '84106', '84107', '84108', '84109', '84111', '84112', '84113', '84115', '84116', '84117', '84118', '84119', '84120', '84121', '84123', '84124', '84128', '84144', '84180', '84070', '84092', '84093', '84094', '84095', '84081', '84084', '84088']
	utahZipcodes = ['84004', '84003', '84013', '84020', '84005', '84626', '84629', '84633', '84526', '84043', '84042', '84664', '84057', '84058', '84097', '84651', '84062', '84601', '84604', '84606', '84653', '84655', '84045', '84660', '84663']
	wasatchZipcodes = ['84032', '84036', '84049', '84060', '84604', '84082']
 	
	data = request.json
	print(data, data['houseNum'], data['streetName'], data['zipcode'])
	print('invoking POST SCRAPE')

	result = {}
	if data['zipcode'] in saltZipcodes:
		result['accessor'] = scrape_salt.scrapeSalt(data['houseNum'], data['streetName'])
	elif data['zipcode'] in utahZipcodes:
		result['accessor'] = scrape_utah.scrapeUtah(data['houseNum'], data['streetName'])
	elif data['zipcode'] in wasatchZipcodes:
		result['accessor'] = scrape_wasatch.scrapeWasatch(data['houseNum'], data['streetName'])
	else:
		result['accessor'] = {
			'error': True
		}

	result['redfin'] = scrape_redfin.scrapeRedfin(data['houseNum'], data['streetName'], data['zipcode'])

	print(result)
	return jsonify(result)



if __name__ == '__main__':
	app.run(host='localhost', port=5000)