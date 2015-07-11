__author__ = 'james'

import sys
from PyQt4 import QtGui, QtCore


class Arthr(QtGui.QMainWindow):

    def __init__(self):
        super(Arthr, self).__init__()

        self.statusBar().showMessage('Ready')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Arthr v2.0')
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Arthr()
    sys.exit(app.exec_())
