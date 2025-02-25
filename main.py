#!/usr/bin/env python3
"""
HTML and Text File Processor - Main Application
Author: Piotr Proszowski
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import FileProcessorWindow

def main():
    app = QApplication(sys.argv)
    window = FileProcessorWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 