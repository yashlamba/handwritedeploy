import os
import shutil
import tempfile
from flask import Flask, request, send_file

import numpy as np
import cv2

from handwrite.cli import converters

app = Flask(__name__)


@app.route("/handwrite/test", methods=["POST"])
def receive_image():
    temp_dir = tempfile.mkdtemp()
    imgarr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)
    cv2.imwrite(os.path.join(temp_dir, "temp.jpg"), img)
    converters(
        os.path.join(temp_dir, "temp.jpg"),
        os.path.join(temp_dir, "temp"),
        os.path.join(temp_dir, "temp"),
        os.path.dirname(os.path.abspath(__file__)) + "/default.json",
    )
    fontfile = send_file(
        os.path.join(temp_dir, "temp", "MyFont.ttf"), as_attachment=True
    )
    shutil.rmtree(temp_dir)
    return fontfile


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
