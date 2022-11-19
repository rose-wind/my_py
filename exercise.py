import sys
from PyQt5.QtWidgets import QApplication,QWidget

if __name__ == '__main__':
    app=QApplication(sys.argv)
    W=QWidget()
    W.setWindowTitle("第一个pyqt")
    W.show()
    app.exec_()