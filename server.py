from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/process/type/<id>", methods=["GET"])
def get_process_type(id):
    if id is 1:
        histogram_equalization()
    elif id is 2:
        contrast_switch()
    elif id is 3:
        log_compression()
    elif id is 4:
        reverse_video()
    else:
        return jsonify('Not a valid ID')
    return jsonify('YAY!')


def histogram_equalization():
    return


def contrast_switch():
    return


def log_compression():
    return


def reverse_video():
    return
