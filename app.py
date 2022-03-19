from flask import Flask, redirect,jsonify, url_for, request
import numpy as np
import cv2

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        print(img)
        return jsonify({"status":200, "message" : "Sudoku Solved"})
    else:
        return "Pfggg"
    

if __name__ == "__main__":
    app.run(debug=True)