import pathlib
import shutil


def exists(s):
    path = pathlib.Path(s)
    if path.exists():
        return
        # print("File exist")
    else:
        source = "./assets/empty.json"
        dest = shutil.copy(source, s)
