from flask import Flask, jsonify, request
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import logging
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')
app = Flask(__name__)


class ImageDB(MongoModel):
    patient_id = fields.CharField(primary_key=True)
    original = fields.ImageField()
    actions = fields.ListField()
    histogram_count = fields.IntegerField()
    contrast_count = fields.IntegerField()
    log_count = fields.IntegerField()
    reverse_count = fields.IntegerField()
    images = fields.ListField()
    processor = fields.ListField()
    images_time_stamp = fields.ListField()


@app.route("/", methods=["GET"])
def greeting():
    """ Welcomes user to image processor

    This function returns the following string: "Welcome to the image
    processor"

    Returns:
        welcome (string): "Welcome to the image processor"
    """

    welcome = "Welcome to the image processor"
    return jsonify(welcome)


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
                 }
    return jsonify(dict_array)


@app.route("/new_image", methods=["POST"])
def add_image():
    """

    Args:

    Returns:

    """

    now = datetime.datetime.now()
    data_in = request.get_json()
    required_image_keys = [

    ]
    for key in required_image_keys:
        if key not in data_in.keys():
            raise ValueError("Key '{}' is missing"
                             " to initialize image"
                             " in imageprocessor".format(key))
    u = ImageDB(
             )
    logging.debug("Image {} was"
                  " successfully initialized".format(u.name))
    u.save()
    return u.name


@app.route("/process", methods=["POST"])
def choose_process():
    r = request.get_json()
    patient_id = r['patient_id']
    process_id = r['process_id']
    image_file = r['image_file']
    validate_image(image_file)
    if process_id is 1:
        processor = 'Histogram Equalization'
        processed_image = histogram_equalization(image_file)
    elif process_id is 2:
        processor = 'Contrast Switch'
        processed_image = contrast_switch(image_file)
    elif process_id is 3:
        processor = 'Log Compression'
        processed_image = log_compression(image_file)
    elif process_id is 4:
        processor = 'Reverse Video'
        processed_image = reverse_video(image_file)
    elif process_id is 0:
        processor = 'Raw Image'
        processed_image = image_file
    else:
        return jsonify('Not a valid ID')
    save_image(patient_id, processor, processed_image)
    return jsonify('YAY!')


def validate_image(image_file):
    return


def save_image(patient_id, processor, image_file):
    patient = ImageDB.objects.raw({"_id": int(patient_id)}).first()
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
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return image_bytes


def encode_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def histogram_equalization(image_file):
    processed_image = 1
    return processed_image


def contrast_switch(image_file):
    processed_image = 1
    return processed_image


def log_compression(image_file):
    processed_image = 1
    return processed_image


def reverse_video(image_file):
    processed_image = 1
    return processed_image


if __name__ == "__main__":
    connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
    # app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
