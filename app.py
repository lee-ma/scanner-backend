from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import img2pdf
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
    pdf = img2pdf.convert(img)
    return send_file(pdf, mimetype="application/pdf")

if __name__ == '__main__':
   app.run(debug = False)