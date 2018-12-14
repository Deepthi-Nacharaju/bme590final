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
from datetime import timedelta
import requests
import base64
import io
import json
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import os
from PIL import Image

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
        """

        Initializes the User Interface with all
        of the appropriate labels and buttons
        :return:
        """
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
        self.notes_label.setText('Upload with Notes:')
        self.notes_label.adjustSize()

        # Create Label for Patient_ID Box
        self.label = QLabel(self)
        self.label.setText('Patient ID:')
        self.label.move(10, 15)

        # Create Open button to open image file
        self.button_open = QPushButton('Open', self)
        self.button_open.move(125, 275)
        self.button_open.setEnabled(False)
        # Create clear button for OG image file
        # self.button_clear = QPushButton('Clear', self)
        # self.button_clear.move(225, 270)

        # connect button to function on click clear OG
        # self.button_clear.clicked.connect(self.on_click_clear_OG)

        # Create clear button for processed image file
        # self.button_clear_process = QPushButton('Clear', self)
        # self.button_clear_process.move(605, 270)

        # connect button to function on_click
        # self.button_clear_process.clicked.connect(
        #    self.on_click_clear_processed)

        # Create save button for processed image file JPEG
        self.button_JPEG = QPushButton('JPEG', self)
        self.button_JPEG.move(505, 270)
        self.button_JPEG.clicked.connect(self.on_click_JPEG)

        # Create save button for processed image file PNG
        self.button_PNG = QPushButton('PNG', self)
        self.button_PNG.move(505, 295)
        self.button_PNG.clicked.connect(self.on_click_PNG)

        # Create save button for processed image file TIFF
        self.button_TIFF = QPushButton('TIFF', self)
        self.button_TIFF.move(505, 320)
        self.button_TIFF.clicked.connect(self.on_click_TIFF)

        # Create Label for 'Save As:'
        self.label_save_as = QLabel(self)
        self.label_save_as.setText('Save As:')
        self.label_save_as.move(530, 250)

        # Open File dialogue to find save path
        # connect button to function on_click
        self.button_open.clicked.connect(self.openFileNameDialog)

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

        # Create Process State Variable
        self.process_state = 0

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
        self.button_HE.clicked.connect(self.get_request)
        # Contrast Stretching
        self.button_CS = QPushButton('Contrast \n Stretching', self)
        self.button_CS.move(375, 105)
        self.button_CS.resize(110, 60)
        self.button_CS.clicked.connect(self.on_click_CS)
        self.button_CS.clicked.connect(self.get_request)
        # Log Compression
        self.button_LC = QPushButton('Log \n Compression', self)
        self.button_LC.move(375, 155)
        self.button_LC.resize(110, 60)
        self.button_LC.clicked.connect(self.on_click_LC)
        self.button_LC.clicked.connect(self.get_request)
        # Reverse Video
        self.button_RV = QPushButton('Reverse \n Video', self)
        self.button_RV.move(375, 205)
        self.button_RV.resize(110, 60)
        self.button_RV.clicked.connect(self.on_click_RV)
        self.button_RV.clicked.connect(self.get_request)
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

        # Time Label
        self.process_time = QLabel(self)
        self.process_time.move(800, 235)
        self.process_time.adjustSize()

        # Image Size in Pixels
        self.image_size_label = QLabel(self)
        self.image_size_label.setText('Image Size:')
        self.image_size_label.move(135, 310)
        self.image_size_label.adjustSize()
        self.fileName = ''
        try:
            r = requests.get(server)
            self.server_status.setText(r.json())
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Server Failed to Initialize')

        # DISPLAY GET REQUEST INFORMATION
        self.histogram_count_label = QLabel(self)
        self.histogram_count_label.setText('Histogram Count:')
        self.histogram_count_label.adjustSize()
        self.histogram_count_label.move(865, 405)

        self.histogram_count = QLabel(self)
        self.histogram_count.move(975, 405)
        self.histogram_count.setText('')

        self.contrast_count_label = QLabel(self)
        self.contrast_count_label.setText('Contrast Count:')
        self.contrast_count_label.adjustSize()
        self.contrast_count_label.move(865, 430)

        self.contrast_count = QLabel(self)
        self.contrast_count.move(965, 430)
        self.contrast_count.setText('')

        self.log_count_label = QLabel(self)
        self.log_count_label.setText('Log Count:')
        self.log_count_label.adjustSize()
        self.log_count_label.move(865, 455)

        self.log_count = QLabel(self)
        self.log_count.move(937, 455)
        self.log_count.setText('')

        self.reverse_count_label = QLabel(self)
        self.reverse_count_label.setText('Reverse Count:')
        self.reverse_count_label.adjustSize()
        self.reverse_count_label.move(865, 480)

        self.reverse_count = QLabel(self)
        self.reverse_count.setText('')
        self.reverse_count.move(960, 480)

        self.id_status = self.textbox.text()
        self.textbox.textChanged.connect(self.on_click_clear_OG)
        self.textbox.textChanged.connect(self.get_request)

        self.current_image = ''
        self.active_image = ''
        self.original = ''
        self.histogram_count_value = []
        self.contrast_count_value = []
        self.log_count_value = []
        self.reverse_count_value =[]
        self.index = 0

        # Scroll Buttons
        self.right_scroll = QPushButton('->', self)
        self.right_scroll.move(230, 250)
        self.right_scroll.resize(50, 25)
        self.right_scroll.clicked.connect(self.on_click_right_scroll)
        self.right_scroll.clicked.connect(self.get_request)

        self.left_scroll = QPushButton('<-', self)
        self.left_scroll.move(175, 250)
        self.left_scroll.resize(50, 25)
        self.left_scroll.clicked.connect(self.on_click_left_scroll)
        self.left_scroll.clicked.connect(self.get_request)
        self.show()

    @pyqtSlot()
    def openFileNameDialog(self):
        """

        Opens File Dialog to choose image to be processed
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        current = os.getcwd()
        fileName, _ = QFileDialog.getOpenFileNames(self, "Open Image", current,
                                                  "Image files (*.jpg *.png)",
                                                  options=options)
        if fileName:
            self.fileName = fileName
            if len(fileName) > 1:
                pixmap = QPixmap(fileName[0])
                pic_list = list()
                for x in range(len(fileName)):
                    pic_list.append(front_end.encode_file_as_b64(self.fileName[x]))
                self.current_image = pic_list
            else:
                pixmap = QPixmap(fileName)
                self.current_image = front_end.encode_file_as_b64(self.fileName)
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image.setPixmap(pixmap_scale)
            self.label_image.resize(pixmap_scale.width(),
                                    pixmap_scale.height())
            front_end.get_histogram_values(fileName[0], 'original_histogram.jpg')
            pixmap = QPixmap('original_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.OG_image_histogram.setPixmap(pixmap_scale)
            self.OG_image_histogram.resize(pixmap_scale.width(),
                                           pixmap_scale.height())
            self.image_size_label.setText('Image Size: ' +
                                          str(pixmap.width()) +
                                          'x' +
                                          str(pixmap.height()) +
                                          ' pixels')
            self.image_size_label.adjustSize()
            self.original = self.current_image

    @pyqtSlot()
    def get_request(self):
        """

        Makes get request when patient id is changed or when image is processed
        to update the values in the bottom right of the GUI
        :return:
        """
        patient_id = self.textbox.text()
        if not patient_id:
            return
        add = ''
        self.id_status = patient_id
        get_server = server + "data/" + patient_id
        try:
            r = requests.get(get_server)
        except requests.exceptions.RequestException as e:
            self.server_status.setText(add +
                                       'Get Request Error')
            return
        try:
            r = r.json()
            if r == 'DNE':
                self.server_status.setText(add +
                                           'Patient Does Not Exist')
                return
            try:
                if len(r['histogram_count']) > 1:
                    self.histogram_count.setText(str(r['histogram_count'][self.index]))
                    self.histogram_count.adjustSize()
                    self.contrast_count.setText(str(r['contrast_count'][self.index]))
                    self.contrast_count.adjustSize()
                    self.log_count.setText(str(r['log_count'][self.index]))
                    self.log_count.adjustSize()
                    self.reverse_count.setText(str(r['reverse_count'][self.index]))
                    self.reverse_count.adjustSize()
                    self.server_status.setText(add +
                                               'Get Request Successful')
            except TypeError:
                self.histogram_count.setText(str(r['histogram_count']))
                self.histogram_count.adjustSize()
                self.contrast_count.setText(str(r['contrast_count']))
                self.contrast_count.adjustSize()
                self.log_count.setText(str(r['log_count']))
                self.log_count.adjustSize()
                self.reverse_count.setText(str(r['reverse_count']))
                self.reverse_count.adjustSize()
                self.server_status.setText(add +
                                           'Get Request Successful')
            self.histogram_count_value = r['histogram_count']
            self.contrast_count_value = r['contrast_count']
            self.log_count_value = r['log_count']
            self.reverse_count_value = r['reverse_count']

        except json.decoder.JSONDecodeError:
            self.server_status.setText(add +
                                       'Get Request Decode Error')

    @pyqtSlot()
    def open_error(self):
        """

        Opens Error Window if image is not chosen
        :return:
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Must open an image')
        msg.setWindowTitle('Error')
        msg.exec()

    @pyqtSlot()
    def no_patient_error(self):
        """

        Opens error window when patient ID is not provided
        :return:
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Must enter a patient ID')
        msg.setWindowTitle('Error')
        msg.exec()

    @pyqtSlot()
    def on_click_clear_OG(self):
        """

        Updates image spaces with last procssed image
        for the specified patient ID
        :return:
        """
        patient_id = self.textbox.text()
        if not patient_id:
            return
        get_server = server + "data/last/" + patient_id
        try:
            r = requests.get(get_server)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Get Request Error')
            return
        try:
            r = r.json()
            if r == 'DNE':
                self.server_status.setText('Patient Does Not Exist')
                pixmap = QPixmap('white.png')
                pixmap_scale = pixmap.scaled(256, 256,
                                             QtCore.Qt.KeepAspectRatio)
                self.label_image.setPixmap(pixmap_scale)
                self.label_image.resize(pixmap_scale.width(),
                                        pixmap_scale.height())
                pixmap_scale = pixmap.scaled(400, 400,
                                             QtCore.Qt.KeepAspectRatio)
                self.OG_image_histogram.setPixmap(pixmap_scale)
                self.OG_image_histogram.resize(pixmap_scale.width(),
                                               pixmap_scale.height())
                pixmap_scale = pixmap.scaled(256, 256,
                                             QtCore.Qt.KeepAspectRatio)
                self.label_image_processed.setPixmap(pixmap_scale)
                self.label_image_processed.resize(pixmap_scale.width(),
                                                  pixmap_scale.height())
                pixmap_scale = pixmap.scaled(400, 400,
                                             QtCore.Qt.KeepAspectRatio)
                self.processed_image_histogram.setPixmap(pixmap_scale)
                self.processed_image_histogram.resize(pixmap_scale.width(),
                                                      pixmap_scale.height())
                self.histogram_count.setText('0')
                self.histogram_count.adjustSize()
                self.contrast_count.setText('0')
                self.contrast_count.adjustSize()
                self.log_count.setText('0')
                self.log_count.adjustSize()
                self.reverse_count.setText('0')
                self.reverse_count.adjustSize()
                self.button_open.setEnabled(True)
                self.current_image = ''
                self.original = ''
                return

        except json.decoder.JSONDecodeError:
            self.server_status.setText('Get Request Decode Error')
        print(len(r['original']))
        if len(r['original']) > 1:
            image_bytes = base64.b64decode(r['original'][0])
        else:
            image_bytes = base64.b64decode(r['original'][0])
        self.original = r['original']

        image_buf = io.BytesIO(image_bytes)
        i = mpimg.imread(image_buf, format='JPG')
        fig = plt.figure(frameon=False)
        plt.imshow(i, interpolation='nearest')
        plt.axis('off')

        plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
        pixmap = QPixmap('save_as_jpg.jpg')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image.setPixmap(pixmap_scale)
        self.label_image.resize(pixmap_scale.width(), pixmap_scale.height())
        front_end.get_histogram_values('save_as_jpg.jpg',
                                       'processed_histogram.jpg')
        pixmap = QPixmap('processed_histogram.jpg')
        pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.OG_image_histogram.setPixmap(pixmap_scale)
        self.OG_image_histogram.resize(pixmap_scale.width(),
                                       pixmap_scale.height())
        self.current_image = r['last_process']
        if len(r['last_process']) > 1:
            image_bytes = base64.b64decode(self.current_image[0])
        else:
            image_bytes = base64.b64decode(self.current_image)
        image_buf = io.BytesIO(image_bytes)
        i = mpimg.imread(image_buf, format='JPG')
        fig = plt.figure(frameon=False)
        plt.imshow(i, interpolation='nearest')
        plt.axis('off')

        plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
        pixmap = QPixmap('save_as_jpg.jpg')
        pixmap_scale = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.label_image_processed.setPixmap(pixmap_scale)
        self.label_image_processed.resize(pixmap_scale.width(),
                                          pixmap_scale.height())
        front_end.get_histogram_values('save_as_jpg.jpg',
                                       'processed_histogram.jpg')
        pixmap = QPixmap('processed_histogram.jpg')
        pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.processed_image_histogram.setPixmap(pixmap_scale)
        self.processed_image_histogram.resize(pixmap_scale.width(),
                                              pixmap_scale.height())
        self.button_open.setEnabled(False)
        self.process_state = 1

    @pyqtSlot()
    def on_click_JPEG(self):
        """

        Saves image as a JPEG
        :return:
        """
        if self.process_state == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Process Image First')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save JPEG",
                                                  os.getcwd(),
                                                  "Image files (*.jpg)")
        if fileName:
            save_image = Image.open('save_as_jpg.jpg')
            save_image.save(fileName, 'JPEG')

    @pyqtSlot()
    def on_click_PNG(self):
        """

        Saves image as a PNG
        :return:
        """
        if self.process_state == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Process Image First')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save PNG",
                                                  os.getcwd(),
                                                  "Image files (*.png)")
        if fileName:
            save_image = Image.open('save_as_jpg.jpg')
            save_image.save(fileName, 'PNG')

    @pyqtSlot()
    def on_click_TIFF(self):
        """

        Saves image as a TIFF
        :return:
        """
        if self.process_state == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Process Image First')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save TIFF",
                                                  os.getcwd(),
                                                  "Image files (*.tif)")
        if fileName:
            server_tif = server + 'data/stack/<patient_id>'
            r = requests.get(server_tif)
            r = r.json()
            for image in r:
                save_image = Image.open('save_as_jpg.jpg')
                save_image.save(fileName, save_all=True)

    @pyqtSlot()
    def on_click_HE(self):
        """

        Applies Histogram Equalization to original
        image and makes a POST request to the server
        :return:
        """
        one_time = datetime.datetime.now()
        server_HE = server + 'new_image'
        if not self.notes.toPlainText():
            notes = 'No Additional Notes'
        else:
            notes = self.notes.toPlainText()
        if self.current_image == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Open Image')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        if self.current_image == '':
            self.open_error
            return
        if self.textbox.text() == "":
            self.no_patient_error()
        post_dict = {
            'patient_id': str(self.textbox.text()),
            'process_id': 1,
            'image_file': self.current_image,
            'original': self.original,
            'notes': notes
        }
        if len(post_dict['original']) > 1:
            post_dict['index'] = self.index
        try:
            r = requests.post(server_HE, json=post_dict)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Connection Failure')
        try:
            p_image = 'decode.jpg'
            # front_end.decode_b64_image(r.json(), p_image)
            self.current_image = r.json()
            if len(self.current_image) > 1:
                image_bytes = base64.b64decode(self.current_image[self.index])
            else:
                image_bytes = base64.b64decode(self.current_image)
            image_buf = io.BytesIO(image_bytes)
            i = mpimg.imread(image_buf, format='JPG')
            fig = plt.figure(frameon=False)
            plt.imshow(i, interpolation='nearest')
            plt.axis('off')

            plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
            pixmap = QPixmap('save_as_jpg.jpg')
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image_processed.setPixmap(pixmap_scale)
            self.label_image_processed.resize(pixmap_scale.width(),
                                              pixmap_scale.height())
            front_end.get_histogram_values('save_as_jpg.jpg',
                                           'processed_histogram.jpg')
            pixmap = QPixmap('processed_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.processed_image_histogram.setPixmap(pixmap_scale)
            self.processed_image_histogram.resize(pixmap_scale.width(),
                                                  pixmap_scale.height())
            self.server_status.setText('Successful')
            self.time_stamp_label.setText(datetime.datetime.now().strftime(
                "%m-%d-%Y %I:%M%p"))
            self.time_stamp_label.adjustSize()
            two_time = datetime.datetime.now()
            time_delta = two_time - one_time
            self.process_time.setText(str(time_delta))
            self.process_time.adjustSize()
            self.process_state = 1
        except json.decoder.JSONDecodeError:
            self.server_status.setText('Server Returned Nothing')

    @pyqtSlot()
    def on_click_CS(self):
        """

        Applies Contrast Stretching to original
        image and makes a POST request to the server
        :return:
        """
        if not self.notes.toPlainText():
            notes = 'No Additional Notes'
        else:
            notes = self.notes.toPlainText()
        if self.current_image == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Open Image')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        one_time = datetime.datetime.now()
        server_HE = server + 'new_image'
        if self.current_image == '':
            self.open_error
            return
        if self.textbox.text() == "":
            self.no_patient_error()
        post_dict = {
            'patient_id': str(self.textbox.text()),
            'process_id': 2,
            'image_file': self.current_image,
            'original': self.original,
            'notes': notes
        }
        if len(post_dict['original']) > 1:
            post_dict['index'] = self.index
        try:
            r = requests.post(server_HE, json=post_dict)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Connection Failure')
        try:
            p_image = 'decode.jpg'
            # front_end.decode_b64_image(r.json(), p_image)
            self.current_image = r.json()
            image_bytes = base64.b64decode(self.current_image[self.index])
            image_buf = io.BytesIO(image_bytes)
            i = mpimg.imread(image_buf, format='JPG')
            fig = plt.figure(frameon=False)
            plt.imshow(i, interpolation='nearest')
            plt.axis('off')

            plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
            pixmap = QPixmap('save_as_jpg.jpg')
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image_processed.setPixmap(pixmap_scale)
            self.label_image_processed.resize(pixmap_scale.width(),
                                              pixmap_scale.height())
            front_end.get_histogram_values('save_as_jpg.jpg',
                                           'processed_histogram.jpg')
            pixmap = QPixmap('processed_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.processed_image_histogram.setPixmap(pixmap_scale)
            self.processed_image_histogram.resize(pixmap_scale.width(),
                                                  pixmap_scale.height())
            self.server_status.setText('Successful')
            self.time_stamp_label.setText(datetime.datetime.now().strftime(
                "%m-%d-%Y %I:%M%p"))
            self.time_stamp_label.adjustSize()
            two_time = datetime.datetime.now()
            time_delta = two_time - one_time
            self.process_time.setText(str(time_delta))
            self.process_time.adjustSize()
            self.process_state = 1
        except json.decoder.JSONDecodeError:
            self.server_status.setText('Server Returned Nothing')

    @pyqtSlot()
    def on_click_LC(self):
        """

        Applies Log Compression to original image and
        makes a POST request to the server
        :return:
        """
        if not self.notes.toPlainText():
            notes = 'No Additional Notes'
        else:
            notes = self.notes.toPlainText()
        if self.current_image == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Open Image')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        one_time = datetime.datetime.now()
        server_HE = server + 'new_image'
        if self.current_image == '':
            self.open_error
            return
        if self.textbox.text() == "":
            self.no_patient_error()
        post_dict = {
            'patient_id': str(self.textbox.text()),
            'process_id': 3,
            'image_file': self.current_image,
            'original': self.original,
            'notes': notes
        }
        if len(post_dict['original']) > 1:
            post_dict['index'] = self.index
        try:
            r = requests.post(server_HE, json=post_dict)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Connection Failure')
        try:
            p_image = 'decode.jpg'
            # front_end.decode_b64_image(r.json(), p_image)
            self.current_image = r.json()
            print('Length of current image array:')
            print(len(self.current_image))
            image_bytes = base64.b64decode(self.current_image[self.index])
            image_buf = io.BytesIO(image_bytes)
            i = mpimg.imread(image_buf, format='JPG')
            fig = plt.figure(frameon=False)
            plt.imshow(i, interpolation='nearest')
            plt.axis('off')

            plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
            pixmap = QPixmap('save_as_jpg.jpg')
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image_processed.setPixmap(pixmap_scale)
            self.label_image_processed.resize(pixmap_scale.width(),
                                              pixmap_scale.height())
            front_end.get_histogram_values('save_as_jpg.jpg',
                                           'processed_histogram.jpg')
            pixmap = QPixmap('processed_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.processed_image_histogram.setPixmap(pixmap_scale)
            self.processed_image_histogram.resize(pixmap_scale.width(),
                                                  pixmap_scale.height())
            self.server_status.setText('Successful')
            self.time_stamp_label.setText(datetime.datetime.now().strftime(
                "%m-%d-%Y %I:%M%p"))
            self.time_stamp_label.adjustSize()
            two_time = datetime.datetime.now()
            time_delta = two_time - one_time
            self.process_time.setText(str(time_delta))
            self.process_time.adjustSize()
            self.process_state = 1
        except json.decoder.JSONDecodeError:
            self.server_status.setText('Server Returned Nothing')

    @pyqtSlot()
    def on_click_RV(self):
        """

        Applies Reverse Video to original image and
        makes a POST request to the server
        :return:
        """
        if not self.notes.toPlainText():
            notes = 'No Additional Notes'
        else:
            notes = self.notes.toPlainText()
        if self.current_image == '':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Must Open Image')
            msg.setWindowTitle('Error')
            msg.exec()
            return
        one_time = datetime.datetime.now()
        server_HE = server + 'new_image'
        if self.current_image == '':
            self.open_error
            return
        if self.textbox.text() == "":
            self.no_patient_error()
        post_dict = {
            'patient_id': str(self.textbox.text()),
            'process_id': 4,
            'image_file': self.current_image,
            'original': self.original,
            'notes': notes
        }
        if len(post_dict['original']) > 1:
            post_dict['index'] = self.index
        try:
            r = requests.post(server_HE, json=post_dict)
        except requests.exceptions.RequestException as e:
            self.server_status.setText('Connection Failure')
        try:
            p_image = 'decode.jpg'
            # front_end.decode_b64_image(r.json(), p_image)
            self.current_image = r.json()
            image_bytes = base64.b64decode(self.current_image[self.index])
            image_buf = io.BytesIO(image_bytes)
            i = mpimg.imread(image_buf, format='JPG')
            fig = plt.figure(frameon=False)
            plt.imshow(i, interpolation='nearest')
            plt.axis('off')

            plt.savefig('save_as_jpg.jpg', bbox_inches='tight', pad_inches=0)
            pixmap = QPixmap('save_as_jpg.jpg')
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image_processed.setPixmap(pixmap_scale)
            self.label_image_processed.resize(pixmap_scale.width(),
                                              pixmap_scale.height())
            front_end.get_histogram_values('save_as_jpg.jpg',
                                           'processed_histogram.jpg')
            pixmap = QPixmap('processed_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.processed_image_histogram.setPixmap(pixmap_scale)
            self.processed_image_histogram.resize(pixmap_scale.width(),
                                                  pixmap_scale.height())
            self.server_status.setText('Successful')
            self.time_stamp_label.setText(datetime.datetime.now().strftime(
                "%m-%d-%Y %I:%M%p"))
            self.time_stamp_label.adjustSize()
            two_time = datetime.datetime.now()
            time_delta = two_time - one_time
            self.process_time.setText(str(time_delta))
            self.process_time.adjustSize()
            self.process_state = 1
        except json.decoder.JSONDecodeError:
            self.server_status.setText('Server Returned Nothing')


    @pyqtSlot()
    def on_click_right_scroll(self):
        if len(self.original) > 1:
            self.index += 1
            if self.index > len(self.current_image) - 1:
                self.index -= 1
                return
            pixmap = QPixmap(self.fileName[self.index])
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image.setPixmap(pixmap_scale)
            self.label_image.resize(pixmap_scale.width(),
                                    pixmap_scale.height())
            print(self.index)
            front_end.get_histogram_values(self.fileName[self.index], 'original_histogram.jpg')
            pixmap = QPixmap('original_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.OG_image_histogram.setPixmap(pixmap_scale)
            self.OG_image_histogram.resize(pixmap_scale.width(),
                                           pixmap_scale.height())
            self.image_size_label.setText('Image Size: ' +
                                          str(pixmap.width()) +
                                          'x' +
                                          str(pixmap.height()) +
                                          ' pixels')
            self.image_size_label.adjustSize()


    @pyqtSlot()
    def on_click_left_scroll(self):
        if len(self.original) > 1:
            self.index -= 1
            if self.index < 0:
                self.index = 0
                return
            pixmap = QPixmap(self.fileName[self.index])
            pixmap_scale = pixmap.scaled(256, 256,
                                         QtCore.Qt.KeepAspectRatio)
            self.label_image.setPixmap(pixmap_scale)
            self.label_image.resize(pixmap_scale.width(),
                                    pixmap_scale.height())
            front_end.get_histogram_values(self.fileName[self.index], 'original_histogram.jpg')
            pixmap = QPixmap('original_histogram.jpg')
            pixmap_scale = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.OG_image_histogram.setPixmap(pixmap_scale)
            self.OG_image_histogram.resize(pixmap_scale.width(),
                                           pixmap_scale.height())
            self.image_size_label.setText('Image Size: ' +
                                          str(pixmap.width()) +
                                          'x' +
                                          str(pixmap.height()) +
                                          ' pixels')
            self.image_size_label.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
