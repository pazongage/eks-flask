from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from our My Flask app, Thanks Paz Fridman!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')