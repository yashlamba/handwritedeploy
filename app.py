import os
import shutil
import tempfile

import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    # app.config["CORS_HEADERS"] = "Content-Type"

    server_dir = os.path.dirname(os.path.abspath(__file__))
    in_files_dir = os.path.join(server_dir, "infiles")
    out_files_dir = os.path.join(server_dir, "outfiles")
    status_files_dir = os.path.join(server_dir, "status")

    @app.route("/handwrite/input", methods=["POST"])
    def receive_image():
        # TODO Code for when image isn't successfully created, also check exception handlers
        # in Flask
        image = request.files["image"].read()
        imgarr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)

        path = None
        with tempfile.NamedTemporaryFile(dir=in_files_dir) as f:
            cv2.imwrite(f.name + ".jpg", img)
            with open(status_files_dir + os.sep + os.path.basename(f.name), "w") as fs:
                pass
            path = f.name.split(os.sep)[-1]

        if (
            path
            and os.path.exists(in_files_dir + os.sep + path + ".jpg")
            and os.path.exists(status_files_dir + os.sep + path)
        ):
            return jsonify(path=path)
        else:
            return jsonify(error="Bad Request!")

    @app.route("/handwrite/status/<path>")
    def process_status(path):
        """
        Returns:
            0 if Done
            1 if Processing
            2 if Not found in requests
        """
        fontfile, statusfile = (
            os.path.exists(out_files_dir + os.sep + path + os.sep + "MyFont.ttf"),
            os.path.exists(status_files_dir + os.sep + path),
        )

        status = 2
        if fontfile:
            status = 0
        elif statusfile:
            status = 1

        return jsonify(status=status)

    @app.route("/handwrite/fetch/<path>", methods=["POST"])
    def fetch_font(path):
        """
        Returns:
            fontfile if found
            else json with error
        """
        fontpath = out_files_dir + os.sep + path + os.sep + "MyFont.ttf"
        if os.path.exists(fontpath):
            fontfile = send_file(fontpath, as_attachment=True,)
            shutil.rmtree(out_files_dir + os.sep + path)
            return fontfile
        return jsonify(error="File Not Found!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
