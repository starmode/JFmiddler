#!/usr/bin/python3

from window import Dynamics
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myshow = Dynamics()
    myshow.show()
    sys.exit(app.exec_())
