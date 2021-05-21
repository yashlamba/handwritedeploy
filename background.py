import os
import shutil
import tempfile
import time
from handwrite.cli import converters

currQ = []


def handwrite_background():
    in_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "infiles")
    status_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "status")
    out_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outfiles")
    shutil.rmtree(in_files_dir, ignore_errors=True)
    shutil.rmtree(status_files_dir, ignore_errors=True)
    shutil.rmtree(out_files_dir, ignore_errors=True)
    os.makedirs(in_files_dir, exist_ok=True)
    os.makedirs(status_files_dir, exist_ok=True)
    os.makedirs(out_files_dir, exist_ok=True)

    while True:
        if len(currQ) == 0:
            root, dirs, files = next(os.walk(status_files_dir))
            while len(currQ) <= 3 and files:
                currQ.append(files.pop())
        if currQ:
            path = currQ.pop(0) + ".jpg"
            temp_dir = tempfile.mkdtemp()
            os.makedirs(out_files_dir + os.sep + path.split(".")[0])
            # time.sleep(2)
            converters(
                in_files_dir + os.sep + path,
                temp_dir,
                out_files_dir + os.sep + path.split(".")[0],
                os.path.dirname(os.path.abspath(__file__)) + "/default.json",
            )
            os.remove(in_files_dir + os.sep + path)
            os.remove(status_files_dir + os.sep + path.split(".")[0])
            shutil.rmtree(temp_dir)
