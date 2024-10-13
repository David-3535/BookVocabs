from flask import Flask, render_template, jsonify, request
import cv2
import io
import requests
import json
from PIL import Image
import numpy as np

app = Flask(__name__)

URL_API = "https://api.ocr.space/parse/image"

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/upload", methods = ["POST"])
def imageToText():
   if 'file' not in request.files:
      return jsonify({'error': 'No file part in the request'}), 400
   file = request.files['file']
   if file.filename == '':
      return jsonify({'error': 'No selected file'}), 400
   if file:
      preimg = Image.open(file)
      img = np.array(preimg)

      _, compressedimage = cv2.imencode(".jpg", img, [1, 50])
      file_bytes = io.BytesIO(compressedimage)
      result = requests.post(URL_API,
                             files={"screenshot.jpg": file_bytes},
                             data={"apikey": "K83628016388957",
                                   "language": "eng"})
      result = result.content.decode()
      result = json.loads(result)
      print(result)

      parsed_results = result.get("ParsedResults")[0]
      text_detected = parsed_results.get("ParsedText")
      print(text_detected)
      return jsonify({'message': 'File uploaded successfully', 'data': text_detected}), 200


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)