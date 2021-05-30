import tempfile
import os
import sys
import shutil
from handwrite.cli import converters


def main_process(path, out_file_dir):
    temp_dir = tempfile.mkdtemp()
    os.makedirs(out_file_dir + os.sep + path.split(os.sep)[-1].split(".")[0])
    converters(
        path,
        temp_dir,
        out_file_dir + os.sep + path.split(os.sep)[-1].split(".")[0],
        os.path.dirname(os.path.abspath(__file__)) + "/default.json",
    )
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main_process(sys.argv[1], sys.argv[2])
