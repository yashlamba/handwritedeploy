import os
import shutil
import tempfile
from flask import Flask, request, send_file, jsonify, abort
from flask.wrappers import Response
import gc
import subprocess

import numpy as np
import cv2
from hashlib import sha256
from handwrite.cli import converters
import threading


# semaphore = threading.Semaphore(5)


class IO:
    def __init__(self):
        self.in_files_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "infiles"
        )
        self.out_file_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "outfiles"
        )
        os.makedirs(self.in_files_dir, exist_ok=True)
        os.makedirs(self.out_file_dir, exist_ok=True)
        # self.p = 0
        # self.q = []
        # x = threading.Thread(target=self.force_start)
        # x.start()

    def add_image(self, imgarr):
        img = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)
        with tempfile.NamedTemporaryFile(dir=self.in_files_dir) as f:
            cv2.imwrite(f.name + ".jpg", img)
            with open("status" + os.sep + os.path.basename(f.name), "w") as fs:
                pass
            # self.q.append(f.name + ".jpg")
            # process = threading.Thread(
            #     target=main_process, args=(f.name + ".jpg", self.out_file_dir[:],)
            # )
            # process.daemon = True
            # process.start()
            # subprocess.Popen(
            #     ["python", "mainprocess.py", f.name + ".jpg", self.out_file_dir]
            # )
            return f.name.split(os.sep)[-1]

    def check_font(self, path):
        return os.path.exists(self.out_file_dir + os.sep + path + ".ttf")

    # def force_start(self):
    #     while True:
    #         # gc.collect()
    #         # print(threading.active_count(), "\t", self.p)
    #         if self.q:
    #             self.main_process(self.q.pop(0))
    #             # t = threading.Thread(target=self.main_process, args = (self.q.pop(0),))
    #             # t.start()

    # semaphore.release()
    # self.p -= 1

    def font_path(self, path):
        return self.out_file_dir + os.sep + path + ".ttf"


def create_app():
    app = Flask(__name__)

    app.config["IO"] = IO()

    @app.route("/handwrite/test", methods=["POST"])
    def receive_image():
        app.logger.info("requested")
        in_files_dir = os.path.dirname(os.path.abspath(__file__))
        imgarr = np.frombuffer(request.data, np.uint8)
        path = app.config["IO"].add_image(imgarr)

        return jsonify({"path": path})

    @app.route("/handwrite/<path>")
    def process_status(path):
        if app.config["IO"].check_font(path + os.sep + "MyFont"):
            return "Done"
        else:
            return "Not Yet"

    @app.route("/handwrite/fetch/<path>", methods=["POST"])
    def fetch_font(path):
        if app.config["IO"].check_font(path + os.sep + "MyFont"):
            fontfile = send_file(
                app.config["IO"].font_path(path + os.sep + "MyFont"),
                as_attachment=True,
            )
            shutil.rmtree(app.config["IO"].out_file_dir + os.sep + path)
            # os.remove(app.config["IO"].in_files_dir + os.sep + path + ".jpg")
            return fontfile
        else:
            abort(404)

    return app


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
    # app.config["IO"] = IO()
    # port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run()
