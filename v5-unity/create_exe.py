import os
import sys
from PyInstaller import __main__ as PyInstallerMain
from shutil import copyfile

def deal():

    sys.argv = [sys.argv[0], "--onefile", "bottle_server.py"]
    PyInstallerMain.run()
    copyfile("dist/bottle_server.exe", "bottle_server.exe")

    '''
        mv ./dist/bottle_server.exe ./
        tar cfv run.tar ./bottle_server.exe  ./visualize.html ./build/visualize.bundle.js ./favicon.ico ./web_exec_py3.py ./viz_interaction.py
    '''

def main():
    oldpath = os.getcwd()
    newpath = os.path.dirname(__file__)
    os.chdir(newpath)
    deal()
    os.chdir(oldpath)

if __name__ == "__main__":
    pass
