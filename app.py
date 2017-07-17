from flask import Flask
from flask import jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sales_data'
app.config['MONGO_URI'] = 'mongodb://charles:password@ds161042.mlab.com:61042/sales_data'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    return 'OK!'


if __name__ == '__main__':
    app.run(debug=True)
    
