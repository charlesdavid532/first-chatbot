from __future__ import print_function
import json
import os, sys, json, requests
from flask import Flask, request, make_response
from flask import jsonify
from flask.ext.pymongo import PyMongo
from pymessenger import Bot
from datetime import datetime as dt


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)

# Client Access Token for accessing our API AI Bot
CLIENT_ACCESS_TOKEN = 'a9907c0d130e42f2a4c9c328a151d119'

PAGE_ACCESS_TOKEN = "EAABlZAhiLCzsBAEPENnZC43ODWjX1X4VT43TBjHP8dx8WC7W6kqVRLiRz5AljcmkxSk1rfD2ZA4dDdE149D8JIurZBM67Afl6MRFyZBmqH55mTbJTSbHAjKlHSQrHGITB129ekYkdLqGb2ZBJnN7vyEH4HjgPiXzZAO0yW9wj3WXwZDZD"

# An endpoint to ApiAi, an object used for making requests to a particular agent.
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


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

'''
@app.route('/', methods=['POST'])
def handle_message():
    data = request.get_json()
    print(data)
    sys.stdout.flush()

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):

                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = messaging_text
                    bot.send_text_message(sender_id, response)
    
    return "ok", 200 
'''

# Handling HTTP POST when APIAI sends us a payload of messages that have
# have been sent to our bot. 
@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()
    print("Request:")
    print(json.dumps(data, indent=4))
    res = processRequest(data)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

    ''' 
    if data["object"] == "page":
        print("page")
        # Iterating through entries and messaging events batched and sent to us by Messenger
        for entry in data["entry"]:
            print("in entry")
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # Checking if the messaging even contains a message field.
                    print("works")
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    send_message_staggered(sender_id, parse_natural_text(message_text)) # Sending a response to the user.
 
    return "ok", 200 
    '''
 

def processRequest(req):
    print('hi')
    if req.get("result").get("action") == "sales.statistics":
        myCustomResult = getParameters(req)
        res = makeWebhookResult(myCustomResult)
    elif req.get("result").get("action") == "time.timeperiod":
        ''' TODO REMOVE
        myCustomResult = getDummyParameters(req)
        res = makeWebhookResult(myCustomResult)
        '''
        return {}
    else:
        return {}
    return res
'''
This is a very temp function. It is used to just create a sample response in JSON format
'''
def makeWebhookResult(data):
    speech = data
    '''
    print("Response:")
    print(speech)
    '''
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "first-chatbot"
    }
    

def getParameters(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    print("The city is:")
    print(city)
    '''
    duration = parameters.get("Duration")
    print("The duration is:")
    print(duration)
    sales = queryData(city, duration)
    '''
    period = parameters.get("period")
    print("The period is:")
    print(period)
    sales = parsePeriod(period, city)
    print("The sales are:")
    print(sales)
    
    '''return "The sales data for " + city + "and duration" + duration + "is 12345"'''
    return "The sales data for " + city + " and duration " + period + " is " + sales
    '''return "abcd"'''

'''
TODO: REMOVE
'''
def getDummyParameters(req):
    result = req.get("result")
    parameters = result.get("parameters")
    period = parameters.get("period")
    print("The period is:")
    print(period)
    amount = parsePeriod(period)
    
    return "The amount for this duration is " + amount
    

def parsePeriod(period, city):
    '''print ("Period at index 0 is:" + period[0])'''
    '''print ("trying to get date at index 0" + period[0].get('date'))'''
    if period.get('date') != None:
        return queryDataForDate(period.get('date'), city)
    elif period.get('date-period') != None:
        return queryDateForDateRange(period.get('date-period'), city)
    else:
        return 'does not exist in the database'
                                     
def queryDateForDateRange(datePeriod, city):
    print("Inside Query for Date Period")
    startDate = datePeriod.split('/')[0]
    print ("The start date is:" + startDate)
    endDate = datePeriod.split('/')[1]
    print ("The end date is:" + endDate)
    startAmount = None
    amount = 0
    sale = mongo.db.sales  
    
    try: 
        for s in sale.find({'city': city}):
            print ("The date is:" + s['date'])
            if (dt.strptime(s['date'], "%Y-%m-%d") >= dt.strptime(startDate, "%Y-%m-%d")) and (dt.strptime(s['date'], "%Y-%m-%d") <= dt.strptime(endDate, "%Y-%m-%d")):
                print ("Inside if")
                startAmount = 0
                amount = amount + int(s['amount'])
        if startAmount != None:
            return str(amount)
        else:
            return 'not there in the database'
    except Exception:
        print("Could not query database")
        return ''
    

def queryDataForDate(date, city):
    print("Inside Query for Date")
    sale = mongo.db.sales
    startAmount = None
    amount = 0
    
    try: 
        for s in sale.find({'city': city,'date': date}):
            print("The sales amount is:"+s['amount'])
            startAmount = 0
            amount = amount + int(s['amount'])
        if startAmount != None:
            return str(amount)
        else:
            return 'not there in the database'
    except Exception:
        print("Could not query database")
        return ''


# Sending a message back through Messenger.
def send_message(sender_id, message_text):
    print('in send msg')
    r = requests.post("https://api.api.ai/v1/",
 
        
 
        headers={"Content-Type": "application/json"},
 
        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))



# Takes a string of natural language text, passes it to ApiAI, returns a
# response generated by an ApiAI bot.
def parse_natural_text(user_text):
    print('hi there!')
    # Sending a text query to our bot with text sent by the user.
    request = ai.text_request()
    request.query = user_text
 
    # Receiving the response.
    response = json.loads(request.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    if (responseStatus == 200):
        # Sending the textual response of the bot.
        return (response['result']['fulfillment']['speech'])
 
    else:
        return ("Sorry, I couldn't understand that question")
 
    # NOTE:
    # At the moment, all messages sent to ApiAI cannot be differentiated,
    # they are processed as a single conversation regardless of concurrent
    # conversations. We need to perhaps peg a session id (ApiAI) to a recipient
    # id (Messenger) to fix this.
 
    # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
 
# Sends the message in segments delimited by a period.
def send_message_staggered(sender_id, message_text):
    print('staggered') 
    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)
   
    for message in messages:
        send_message(sender_id, message)

@app.route('/add')

def add():
    
    sale = mongo.db.sales
    sale.insert({'city' : 'Mumbai', 'date': 'June', 'amount' : '1900'})
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
    
