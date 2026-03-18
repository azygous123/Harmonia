from PyQt6.QtWidgets import QPlainTextEdit, QWidget


class CodeEditor(QPlainTextEdit):
    def __init__(self):                     # initializer takes no parameters
        super().__init__()                  # runs the superclass init method
        #self.setPlaceholderText("")
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))

#class Vehicle:



