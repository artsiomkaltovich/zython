import os


def read_version():
    while os.path.exists("__init__.py"):
        os.chdir("..")
    with open("changelog.md") as file:
        return file.readline().partition(" ")[-1].rstrip()
