import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QWidget, QPushButton, \
    QAction, QLineEdit, QMessageBox, \
    QLabel, QFileDialog, QTextEdit
from PyQt5.QtGui import *
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import *
import front_end
import datetime
import requests
import base64
import io
import json
server = "http://127.0.0.1:5000/"

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Processor'
        self.left = 10
        self.top = 10
        self.width = 1100
        self.height = 750
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create Patient ID
        self.textbox = QLineEdit(self)
        self.textbox.move(90, 20)
        self.textbox.resize(50, 20)

        # Create notes textbox
        self.notes = QTextEdit(self)
        self.notes.move(800, 75)
        self.notes.resize(250, 100)

        # Create Server Status textbox
        self.server_status = QTextEdit(self)
        self.server_status.move(800, 300)
        self.server_status.resize(250, 50)

        # Server Status Label
        self.notes_label = QLabel(self)
        self.notes_label.move(800, 275)
        self.notes_label.setText('Server Status:')
        self.notes_label.adjustSize()

        # Label Processed Image Space
        self.notes_label = QLabel(self)
        self.notes_label.move(800, 50)
        self.notes_label.setText('Notes:')
        self.notes_label.adjustSize()

        # Create Label for Patient_ID Box
        self.label = QLabel(self)
        self.label.setText('Patient ID:')
        self.label.move(10, 15)

        # Create Upload button in the window
        self.button = QPushButton('Upload', self)
        self.button.move(950, 700)
        # Connect Upload button to time stamp update
        self.button.clicked.connect(self.on_click_Upload)
        self.button.setEnabled(False)

        # Create Open button to open image file
        self.button_open = QPushButton('Open', self)
        self.button_open.move(125, 270)

        # Create clear button for OG image file
        self.button_clear = QPushButton('Clear', self)
        self.button_clear.move(225, 270)

        # connect button to function on click clear OG
        self.button_clear.clicked.connect(self.on_click_clear_OG)

        # Create clear button for processed image file
        self.button_clear_process = QPushButton('Clear', self)
        self.button_clear_process.move(605, 270)

        # connect button to function on_click
        self.button_clear_process.clicked.connect(
            self.on_click_clear_processed)

        # Create save button for processed image file JPEG
        self.button_JPEG = QPushButton('JPEG', self)
        self.button_JPEG.move(505, 270)

        # Create save button for processed image file PNG
        self.button_PNG = QPushButton('PNG', self)
        self.button_PNG.move(505, 295)

        # Create save button for processed image file TIFF
        self.button_TIFF = QPushButton('TIFF', self)
        self.button_TIFF.move(505, 320)

        # Create Label for 'Save As:'
        self.label_save_as = QLabel(self)
        self.label_save_as.setText('Save As:')
        self.label_save_as.move(530, 250)

        # Create Label for 'To Location:'
        self.label_to_location = QLabel(self)
        self.label_to_location.setText('To Location:')
        self.label_to_location.move(610, 292)

        # Create Location Line Edit
        self.textbox_location = QLineEdit(self)
        self.textbox_location.move(610, 320)
        self.textbox_location.resize(130, 20)

        # Open File dialogue to find save path
        # connect button to function on_click
        self.button_open.clicked.connect(self.openFileNameDialog)

        # Create save button for processed image file TIFF
        self.button_choose_location = QPushButton('Choose', self)
        self.button_choose_location.move(680, 292)
        self.button_choose_location.resize(75, 25)

        # Open File dialog
        # connect button to function on_click
        self.button_choose_location.clicked.connect(self.open_choose_location)

        # Label Original Image Space
        self.OG_label = QLabel(self)
        self.OG_label.setText('Original Image')
        self.OG_label.move(180, 15)

        # Label Processed Image Space
        self.OG_label_processed = QLabel(self)
        self.OG_label_processed.move(580, 20)
        self.OG_label_processed.setText('Processed Image')
        self.OG_label_processed.adjustSize()

        # Original Image
        self.label_image = QLabel(self)
        self.label_image.setMaximumWidth(256)
        self.label_image.setMaximumHeight(256)
        self.label_image.move(100, 55)

        # Create background for original image
        pixmap = QPixmap('white.png')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image.setPixmap(pixmap_scale)
        self.label_image.resize(pixmap_scale.width(), pixmap_scale.height())

        # Initialize Processed Image Label
        self.label_image_processed = QLabel(self)
        self.label_image_processed.setMaximumWidth(256)
        self.label_image_processed.setMaximumHeight(256)
        self.label_image_processed.move(500, 55)

        # Create background for processed image
        pixmap = QPixmap('white.png')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image_processed.setPixmap(pixmap_scale)
        self.label_image_processed.resize(pixmap_scale.width(),
                                          pixmap_scale.height())
        # Original Image Histogram
        self.OG_image_histogram = QLabel(self)
        self.OG_image_histogram.setMaximumWidth(400)
        self.OG_image_histogram.setMaximumHeight(400)
        self.OG_image_histogram.move(25, 400)
        pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.OG_image_histogram.setPixmap(pixmap_scale)
        self.OG_image_histogram.resize(pixmap_scale.width(),
                                       pixmap_scale.height())
        # Prcoessed Image Histogram
        self.processed_image_histogram = QLabel(self)
        self.processed_image_histogram.setMaximumWidth(400)
        self.processed_image_histogram.setMaximumHeight(400)
        self.processed_image_histogram.move(450, 400)
        self.processed_image_histogram.setPixmap(pixmap_scale)
        self.processed_image_histogram.resize(pixmap_scale.width(),
                                              pixmap_scale.height())

        # Label Original Image Space histogram
        self.OG_label_histogram = QLabel(self)
        self.OG_label_histogram.setText('Original Color Intensity')
        self.OG_label_histogram.move(150, 370)
        self.OG_label_histogram.adjustSize()

        # Label Original Image Space histogram
        self.processed_label_histogram = QLabel(self)
        self.processed_label_histogram.setText('Processed Color Intensity')
        self.processed_label_histogram.move(575, 370)
        self.processed_label_histogram.adjustSize()

        # Processing Buttons
        # Histogram Equalization
        self.button_HE = QPushButton('Histogram \n Equalization', self)
        self.button_HE.move(375, 55)
        self.button_HE.resize(110, 60)
        self.button_HE.clicked.connect(self.on_click_HE)

        # Contrast Stretching
        self.button_CS = QPushButton('Contrast \n Stretching', self)
        self.button_CS.move(375, 105)
        self.button_CS.resize(110, 60)

        # Log Compression
        self.button_LG = QPushButton('Log \n Compression', self)
        self.button_LG.move(375, 155)
        self.button_LG.resize(110, 60)

        # Reverse Video
        self.button_RV = QPushButton('Reverse \n Video', self)
        self.button_RV.move(375, 205)
        self.button_RV.resize(110, 60)

        # TimeStamp Label Name
        self.time_stamp_name = QLabel(self)
        self.time_stamp_name.setText('Last Upload Time Stamp:')
        self.time_stamp_name.move(800, 175)
        self.time_stamp_name.adjustSize()

        # TimeStamp Label
        self.time_stamp_label = QLabel(self)
        self.time_stamp_label.move(800, 195)
        self.time_stamp_label.adjustSize()

        # Time to Process Image Label
        self.process_time_image = QLabel(self)
        self.process_time_image.setText('Time to Process Image:')
        self.process_time_image.move(800, 215)
        self.process_time_image.adjustSize()

        # Image Size in Pixels
        self.image_size_label = QLabel(self)
        self.image_size_label.setText('Image Size:')
        self.image_size_label.move(135, 300)
        self.image_size_label.adjustSize()
        self.fileName = ''
        self.show()
        try:
            r = requests.get(server)
            self.server_status.setText(r.json())
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Server Failed to Initialize')

    @pyqtSlot()
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", 'c:\\',
                                                  "Image files (*.jpg *.gif)",
                                                  options=options)
        if fileName:
            self.fileName = fileName
            pixmap = QPixmap(fileName)
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image.setPixmap(pixmap_scale)
            self.label_image.resize(pixmap_scale.width(),
                                    pixmap_scale.height())
            front_end.get_histogram_values(fileName, 'original_histogram.jpg')
            pixmap = QPixmap('original_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.OG_image_histogram.setPixmap(pixmap_scale)
            self.OG_image_histogram.resize(pixmap_scale.width(),
                                           pixmap_scale.height())
            self.image_size_label.setText('Image Size: ' +
                                          str(pixmap.height()) +
                                          'x' +
                                          str(pixmap.width()) +
                                          ' pixels')
            self.image_size_label.adjustSize()

    @pyqtSlot()
    def open_choose_location(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(None,
                                                    'Save As',
                                                    'c:\\',
                                                    QFileDialog.ShowDirsOnly)
        if fileName:
            self.textbox_location.setText(fileName)

    @pyqtSlot()
    def open_error(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Must open an image')
        msg.setWindowTitle('Error')
        msg.exec()

    @pyqtSlot()
    def no_patient_error(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Must enter a patient ID')
        msg.setWindowTitle('Error')
        msg.exec()

    @pyqtSlot()
    def on_click_clear_OG(self):
        pixmap = QPixmap('white.png')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image.setPixmap(pixmap_scale)
        self.label_image.resize(pixmap_scale.width(), pixmap_scale.height())
        pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.OG_image_histogram.setPixmap(pixmap_scale)
        self.OG_image_histogram.resize(pixmap_scale.width(),
                                       pixmap_scale.height())
        self.show()

    @pyqtSlot()
    def on_click_clear_processed(self):
        pixmap = QPixmap('white.png')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image_processed.setPixmap(pixmap_scale)
        self.label_image_processed.resize(pixmap_scale.width(),
                                          pixmap_scale.height())
        pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.processed_image_histogram.setPixmap(pixmap_scale)
        self.processed_image_histogram.resize(pixmap_scale.width(),
                                              pixmap_scale.height())

    @pyqtSlot()
    def on_click_Upload(self):
        self.time_stamp_label.setText(datetime.datetime.now().strftime(
            "%m-%d-%Y %I:%M%p"))
        self.time_stamp_label.adjustSize()

    @pyqtSlot()
    def on_click_HE(self):
        server_HE = server + 'new_image'
        try:
            send_string = front_end.encode_file_as_b64(self.fileName)
        except AttributeError:
            self.open_error()
            return
        if self.textbox.text() == "":
            self.no_patient_error()
        post_dict = {
            'patient_id': str(self.textbox.text()),
            'process_id': 1,
            'image_file': send_string,
        }
        try:
            r = requests.post(server_HE, json=post_dict)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Connection Failure')
        try:
            save_name = 'decode.jpg'
            front_end.decode_b64_image(r.json(), save_name)
            pixmap = QPixmap(save_name)
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.processed_image_histogram_image_histogram.setPixmap(pixmap_scale)
            self.processed_image_histogram_image_histogram.resize(pixmap_scale.width(),
                                                                  pixmap_scale.height())
        except json.decoder.JSONDecodeError:
            self.server_status.setText('Server Returned Nothing')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
