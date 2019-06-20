from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from scan import scan

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return 'Hello world!'

@app.route('/scan', methods=['POST'])
def scan_img():
  if request.method == 'POST':
    image = request.json['image']
    img = scan(image)
    return send_file(img)

if __name__ == '__main__':
   app.run(debug = False)