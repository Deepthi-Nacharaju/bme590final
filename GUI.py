import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import front_end

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Processor'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(90, 20)
        self.textbox.resize(50, 20)

        # Create Label for Patient_ID Box
        self.label = QLabel(self)
        self.label.setText('Patient ID:')
        self.label.move(10, 15)

        # Create a button in the window
        self.button = QPushButton('Upload', self)
        self.button.move(650, 250)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message', "You typed: " + textboxValue, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())