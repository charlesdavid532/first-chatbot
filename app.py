from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "OK!", 200

@app.route('/', methods=['POST'])
def postIndex():
    return "Hello world!", 200


if __name__ == '__main__':
    app.run(debug=True, port=80)
    
