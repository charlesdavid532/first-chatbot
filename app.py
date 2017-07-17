import os, sys
from flask import Flask, request
from flask import jsonify
from flask.ext.pymongo import PyMongo
from pymessenger import Bot


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAABlZAhiLCzsBAEPENnZC43ODWjX1X4VT43TBjHP8dx8WC7W6kqVRLiRz5AljcmkxSk1rfD2ZA4dDdE149D8JIurZBM67Afl6MRFyZBmqH55mTbJTSbHAjKlHSQrHGITB129ekYkdLqGb2ZBJnN7vyEH4HjgPiXzZAO0yW9wj3WXwZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

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
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
		sender_id = messaging_event['sender']['id']
		recipient_id = messaging_event['recipient']['id']

		if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

		    # Echo
                    response = messaging_text
                    bot.send_text_message(sender_id, response)

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
    
