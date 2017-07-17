from flask import Flask
from flask import jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sales_data'
app.config['MONGO_URI'] = 'mongodb://charles:password@ds161042.mlab.com:61042/sales_data'

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Hello world!'

@app.route('/add')

def add():
    
    sale = mongo.db.sales
    sale.insert({'city' : 'Faridabad', 'date': '17-July', 'amount' : '1300'})
    return 'Added Sales row'

if __name__ == "__main__":
    app.run()
    
