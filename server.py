from flask import Flask, jsonify, request
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import logging
import base64
import io as io2
import numpy as np
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from skimage import data, io, filters, img_as_float, exposure
from PIL import Image, ImageStat

logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')
app = Flask(__name__)
connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")


class ImageDB(MongoModel):
    patient_id = fields.CharField(primary_key=True)
    actions = fields.ListField()
    histogram_count = fields.IntegerField()
    contrast_count = fields.IntegerField()
    log_count = fields.IntegerField()
    reverse_count = fields.IntegerField()
    images = fields.ListField()
    histogram_values = fields.ListField()
    processor = fields.ListField()
    images_time_stamp = fields.ListField()
    notes = fields.ListField()


@app.route("/", methods=["GET"])
def greeting():
    """ Welcomes user to image processor

    This function returns the following string: "Welcome to the image
    processor"

    Returns:
        welcome (string): "Welcome to the image processor"
    """

    welcome = "Welcome to the image processor!"
    return jsonify(welcome)


@app.route("/new_patient", methods=["POST"])
def add_new_patient():
    r = request.get_json()
    patient = ImageDB(int(r['patient_id']),
                      histogram_count=0,
                      contrast_count=0,
                      log_count=0,
                      reverse_count=0)
    patient.save()
    return jsonify('New Patient Initialized with ID: ' + str(r['patient_id']))


@app.route("/data/<patient_id>", methods=["GET"])
def get_data(patient_id):
    """
    This function returns all the stored information for a patient
    as a JSON dictionary

    Args:
        patient_id (string): string specifying image name.

    Returns:
        dict_array (dict): stored information for specified image
    """
    u = ImageDB.objects.raw({"_id": int(patient_id)}).first()
    dict_array = {
        "patient_id": u.patient_id,
        "original": u.original,
        "actions": u.actions,
        "histogram_count": u.histogram,
        "contrast_count": u.contrast_count,
        "log_count": u.log_count,
        "reverse_count": u.reverse_count,
        "images": u.images,
        "histogram_values": u.histogram_values,
        "processor": u.processor,
        "images_time_stamp": u.images_time_stamp,
        "notes": u.notes
    }
    return jsonify(dict_array)


@app.route("/new_image", methods=["POST"])
def new_image():
    r = request.get_json()
    patient_id = r['patient_id']
    process_id = r['process_id']
    image_file = r['image_file']
    validate_image(image_file)
    patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    if process_id is 1:
        processor = 'Histogram Equalization'
        patient.histogram_count += 1
        processed_image = histogram_equalization(image_file)
    elif process_id is 2:
        processor = 'Contrast Switch'
        patient.contrast_count += 1
        processed_image = contrast_switch(image_file)
    elif process_id is 3:
        processor = 'Log Compression'
        patient.log_count += 1
        processed_image = log_compression(image_file)
    elif process_id is 4:
        processor = 'Reverse Video'
        patient.reverse_count += 1
        processed_image = reverse_video(image_file)
    elif process_id is 0:
        processor = 'Raw Image'
        processed_image = image_file
    else:
        return jsonify('Not a valid ID')
    save_image(patient_id, processor, processed_image)
    return jsonify('Upload Successful for Patient ID: ' + str(r['patient_id']))


def validate_image(image_file):
    try:
        image_file.decode()
    except AttributeError:
        print('Image file is not a "bytes" class.')
    return


def save_image(patient_id, processor, image_file):
    patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    try:
        patient.images.append(image_file)
        patient.save()
    except AttributeError:
        patient.images = image_file
        patient.save()
    try:
        patient.images_time_stamp.append(datetime.datetime.now())
        patient.save()
    except AttributeError:
        patient.images_time_stamp = datetime.datetime.now()
        patient.save()
    try:
        patient.processor.append(processor)
        patient.save()
    except AttributeError:
        patient.processor = processor
        patient.save()
    return


def decode_b64_image(base64_string):
    """
    :param base64_string:
    :return reconstructed_image: PIL image
    """
    from skimage import io as im
    temp = open("temporary.png", "wb")
    temp.write(base64.b64decode(base64_string))
    temp.close()
    reconstructed_image = im.imread("temporary.png")
    #    image_bytes = base64.b64decode(base64_string)
    #    image_buf = io.BytesIO(image_bytes)
    #    i = mpimg.imread(image_buf, format='JPG')
    #    plt.imshow(i, interpolation='nearest')
    #    plt.show()
    return reconstructed_image


def encode_file_as_b64(image_array):
    image = Image.fromarray(image_array)
    buffer = io2.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    image_string = base64.b64encode(image_bytes.decode("utf-8"))
    #    with open(image_path, "rb") as image_file:
    #        return base64.b64encode(image_file.read())
    return image_string


def make_gray(base64_string):
    """

    :param base64_string:
    :return gray_image: PIL image
    """
    from skimage import io as im
    img = open("gray.png", "wb")
    img.write(base64.b64decode(base64_string))
    img.close()
    image = Image.open("gray.png")
    gray_scale = image.convert('LA')
    gray_scale.save('gray.png')
    gray_image = im.imread("gray.png")
    return gray_image


def histogram_equalization(pil_image):
    equalized = exposure.equalize_hist(pil_image.astype('uint8'))
    normalized = 255 * equalized
    processed_image = normalized.astype('uint8')
    return processed_image


def contrast_stretch(pil_image):
    p2 = np.percentile(pil_image, 2)
    p98 = np.percentile(pil_image, 98)
    rescaled_image = exposure.rescale_intensity(pil_image, in_range=(p2, p98))
    return rescaled_image


def log_compression(pil_image):
    processed_image = 1
    return processed_image


def reverse_video(pil_image):
    processed_image = 1
    return processed_image


Image_Formats = [
    "JPEG",
    "PNG",
    "TIFF"
]


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_file_format(requested_format):
    if requested_format not in Image_Formats:
        raise ValidationError("File format '{0}' not supported"
                              .format(requested_format))


def save_as_format(pil_image, file_format, filename):
    """
    This function handles a Pillow image object and converts it to
    a user-specified file format with a user-specified filename and
    saves it as '<filename>.<format>'. The function will return a
    ValidationError if the requested file_format is not supported,
    and use "JPEG" as default.

    :param pil_image: PILLOW image object
    :param file_format: string
    :param filename: string, pathlib.Path object or file object
    :raises: ValidationError - If the requested format is not JPEG, PNG, TIFF
             ValueError -  If the output format could not be determined from
              the file name.
             IOError – If the file could not be written. The file may have been
             created, and may contain partial data.
    """
    try:
        validate_file_format(file_format)
    except ValidationError as inst:
        print(inst.message)
        file_format = "JPEG"
    try:
        check_filename(filename)
    except ValueError:
        print("Incorrect filename")
    pil_image.save(filename, file_format)
    return


def check_filename(filename):
    return True


if __name__ == "__main__":
    connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
    # app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
    dogsJpg = Image.open("Dogs.jpg", mode='r')
    # dogsJpg = np.asarray(Image.open("Dogs.jpg", mode='r'))
    # opens PIL image as a ndarray
    encoded = encode_file_as_b64(dogsJpg) # induces UnicodeDecodeError
    # im = PIL.Image.fromarray(numpy.uint8(I))
    # converts ndarray to Pillow image
    save_as_format(dogsJpg, "BMP", 'Doggo')
