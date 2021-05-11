import pathlib


def exists(s):
    path = pathlib.Path(s)
    if path.exists():
        return
        # print("File exist")
    else:
        f = open(s, "w+")
        f.write("")
        f.close()
