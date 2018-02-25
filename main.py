#!/bin/env python3
# -*- coding: utf-8 -*-

import cgitb
from PyQt5.QtWidgets import QApplication
from window import Dynamics

if __name__ == "__main__":
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myshow = Dynamics()
    myshow.show()
    sys.exit(app.exec_())
