#!/bin/python3
#--------------------------------------------
#convert .ui to .py
# - open terminal
# - pip install pyuic5 
# - pyuic5 xyz.ui -o xyz.py
#
#


from PyQt5 import QtCore, QtGui, QtWidgets
from setting_gui_v1 import Ui_MainWindow
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(ApplicationWindow, self).__init__()

                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

def main():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('service.png'))
        #app.setWindowTitle('ANPR setting')
        application = ApplicationWindow()
        application.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
