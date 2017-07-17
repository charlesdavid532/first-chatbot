import os, sys
from flask import Flask, request
from flask import jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sales_data'
app.config['MONGO_URI'] = 'mongodb://charles:password@ds161042.mlab.com:61042/sales_data'

mongo = PyMongo(app)

'''
@app.route('/')
def index():
    return 'Hello world!'
'''

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world I am Charles", 200

@app.route('/', methods=['POST'])
def handle_message():
    data = request.get_json()
    print(data)
    sys.stdout.flush()
    return "ok", 200 


@app.route('/add')

def add():
    
    sale = mongo.db.sales
    sale.insert({'city' : 'Faridabad', 'date': '17-July', 'amount' : '1300'})
    return 'Added Sales row'

@app.route('/query')
def query():
    sale = mongo.db.sales
    output = []
    for s in sale.find({'city': 'Pune'}):
        output.append({'city' : s['city'], 'date' : s['date'], 'amount': s['amount']})
    return jsonify({'output':output})

if __name__ == "__main__":
    app.run()
    '''app.run(debug = True, port = 80)'''
    
