#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cgitb import enable
from PyQt5.QtWidgets import QApplication
from window import Dynamics

if __name__ == "__main__":
    import sys

    enable(format='text')
    app = QApplication(sys.argv)
    myshow = Dynamics()
    myshow.show()
    sys.exit(app.exec_())
