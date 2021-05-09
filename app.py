from flask import Flask, request, Response, send_file
import numpy as np
from handwrite.cli import converters
import cv2
import os
import json

app = Flask(__name__)


@app.route("/handwrite/test", methods=["POST"])
def receive_image():
    imgarr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)
    cv2.imwrite("temp.jpg", img)
    converters(
        "temp.jpg",
        os.path.dirname(os.path.abspath(__file__)) + "/temp",
        os.path.dirname(os.path.abspath(__file__)) + "/temp",
        os.path.dirname(os.path.abspath(__file__)) + "/default.json",
    )
    return send_file("temp/MyFont.ttf", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
