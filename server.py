from flask import Flask, jsonify, request
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
app = Flask(__name__)


class ImageDB(MongoModel):
    images = fields.ListField()


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


def save_image(image_file):
    image_list = ImageDB.objects.first()
    try:
        image_list.images.append(image_file)
        image_list.save()
    except AttributeError:
        image_list.images = image_file
        image_list.save()
    return


def histogram_equalization(image_file):
    return


def contrast_switch(image_file):
    return


def log_compression(image_file):
    return


def reverse_video(image_file):
    return
