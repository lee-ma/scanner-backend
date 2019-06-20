from flask import Flask, request
from flask_cors import CORS
from scan import scan

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return 'Hello world!'

@app.route('/scan', methods=['POST'])
def scan_img():
  print('hit')
  if request.methods == 'POST':
    image = request.form['image']
    scan(image)
    return True

if __name__ == '__main__':
   app.run(debug = False)