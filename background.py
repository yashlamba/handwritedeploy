import os
import shutil
import tempfile
from handwrite.cli import converters

currQ = []


def handwrite_background():
    in_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "infiles")
    out_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outfiles")
    os.makedirs(in_files_dir, exist_ok=True)
    os.makedirs(out_files_dir, exist_ok=True)

    while True:
        root, dirs, files = next(os.walk("infiles/"))
        if files and len(currQ) < 3:
            for i in range(3 - len(currQ)):
                currQ.append(files.pop())
        else:
            if currQ:
                path = currQ.pop(0)
                temp_dir = tempfile.mkdtemp()
                os.makedirs(out_files_dir + os.sep + path.split(".")[0])
                converters(
                    in_files_dir + os.sep + path,
                    temp_dir,
                    out_files_dir + os.sep + path.split(".")[0],
                    os.path.dirname(os.path.abspath(__file__)) + "/default.json",
                )
                os.remove(in_files_dir + os.sep + path)
                shutil.rmtree(temp_dir)
