import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSlot
import front_end


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Processor'
        self.left = 100
        self.top = 100
        self.width = 1100
        self.height = 750
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

        # Create Upload button in the window
        self.button = QPushButton('Upload', self)
        self.button.move(950, 700)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Create Open button to open image file
        self.button_open = QPushButton('Open', self)
        self.button_open.move(850, 700)

        # Open File dialog
        # connect button to function on_click
        self.button_open.clicked.connect(self.openFileNameDialog)

        # Label Original Image Space
        self.OG_label = QLabel(self)
        self.OG_label.setText('Original Image')
        self.OG_label.move(275, 15)
        # Original Image
        self.label_image = QLabel(self)
        self.label_image.setMaximumWidth(256)
        self.label_image.setMaximumHeight(256)
        self.label_image.move(200, 55)

        self.show()

    @pyqtSlot()
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", 'c:\\',
                                                  "Image files (*.jpg *.gif)",
                                                  options=options)
        if fileName:
            pixmap = QPixmap('Dogs.jpg')
            pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
            self.label_image.setPixmap(pixmap_scale)
            self.label_image.resize(pixmap_scale.width(), pixmap_scale.height())

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