import os
import shutil
import tempfile
from flask import Flask, request, send_file, jsonify
from flask.wrappers import Response

import numpy as np
import cv2
from hashlib import sha256
from handwrite.cli import converters
import threading

app = Flask(__name__)


# Q = []

# class fontforge():
#     self.processes = 0
#     while q:
#         while self.processes < 5:
#             process(q.pop())
#             self.process += 1

#     process()
#         when done:
#             self.processes -= 1


class IO:
    def __init__(self):
        self.in_files_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "infiles"
        )
        self.out_file_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "outfiles"
        )
        self.q = []
        x = threading.Thread(target=self.force_start)
        x.start()

    def add_image(self, imgarr):
        img = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)
        with tempfile.NamedTemporaryFile(dir=self.in_files_dir) as f:
            cv2.imwrite(f.name + ".jpg", img)
            self.q.append(f.name + ".jpg")
            return f.name.split(os.sep)[-1]

    def check_font(self, path):
        return os.path.exists(self.out_file_dir + os.sep + path + ".ttf")

    def force_start(self):
        while True:
            if self.q:
                self.main_process(self.q.pop(0))

    def main_process(self, path):
        with tempfile.TemporaryDirectory() as d:
            print(path)
            converters(
                path,
                os.path.join(d),
                self.out_file_dir + os.sep + path.split(os.sep)[-1].split(".")[0],
                os.path.dirname(os.path.abspath(__file__)) + "/default.json",
            )


@app.route("/handwrite/test", methods=["POST"])
def receive_image():
    app.logger.info("requested")
    in_files_dir = os.path.dirname(os.path.abspath(__file__))
    imgarr = np.frombuffer(request.data, np.uint8)
    print(app.config["IO"])
    path = app.config["IO"].add_image(imgarr)
    # app.config["IO"].force_start()
    # cv2.imwrite(os.path.join(temp_dir, "temp.jpg"), img)
    # converters(
    #     os.path.join(temp_dir, "temp.jpg"),
    #     os.path.join(temp_dir, "temp"),
    #     os.path.join(temp_dir, "temp"),
    #     os.path.dirname(os.path.abspath(__file__)) + "/default.json",
    # )
    # fontfile = send_file(
    #     os.path.join(temp_dir, "temp", "MyFont.ttf"), as_attachment=True
    # )
    # shutil.rmtree(temp_dir)

    return jsonify({"path": path})


@app.route("/handwrite/<path>")
def process_status(path):
    if app.config["IO"].check_font(path + os.sep + "MyFont.ttf"):
        return "Done"
    else:
        return "Not Yet"


# Request ->
#     1. 55 sec response
#     2. TTF generate ->
#           - Handwrite call
#           - Outfile folder: response.ttf
#     3. RAM control
#     4. 5-10 in return file
#
#     Idea and TODO:
#     1. Production server! - WSGI/Gunicorn
#     2. Limit number of fontforge calls/generate limited ttfs
#     3. On a request:
#           1. Save the image and return 200/202
#           2. Generate 2 routes and a key
#                   - handwrite/<key>/<path>
#                        - return outfiles/<path>.ttf
#                   - handwrite/<path>/status_code
#                        - os.exists(outfiles/path)
#                        - return key when 200


if __name__ == "__main__":
    app.config["IO"] = IO()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
