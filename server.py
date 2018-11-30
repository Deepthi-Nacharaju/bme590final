from flask import Flask, jsonify, request
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import logging
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

    now = datetime.now()
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
def get_process_type():
    r = request.get_json()
    process_id = r['process_id']
    image_file = r['image_file']
    validate_image(image_file)
    if process_id is 1:
        histogram_equalization(image_file)
    elif process_id is 2:
        contrast_switch(image_file)
    elif process_id is 3:
        log_compression(image_file)
    elif process_id is 4:
        reverse_video(image_file)
    else:
        return jsonify('Not a valid ID')
    save_image()
    return jsonify('YAY!')


def validate_image(image_file):
    return


def save_image(patient_id, image_file):
    patient = ImageDB.objects.raw({"_id": int(patient_id)}).first()
    try:
        patient.images.append(image_file)
        patient.save()
    except AttributeError:
        patient.images = image_file
        patient.save()
    return


def histogram_equalization(image_file):
    return


def contrast_switch(image_file):
    return


def log_compression(image_file):
    return


def reverse_video(image_file):
    return


if __name__ == "__main__":
    connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
    # app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
