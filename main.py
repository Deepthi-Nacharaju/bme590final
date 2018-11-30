from flask import Flask, jsonify, request
from pymodm import MongoModel, fields, connect
import logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')
connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")


class User(MongoModel):
    """

    This class initializes the stored data fields for the image processor
    Mongo database.

    Attributes:

    """

    name = fields.CharField(primary_key=True)
    original = fields.ImageField()
    actions = fields.ListField()
    histogram_count = fields.IntegerField()
    contrast_count = fields.IntegerField()
    log_count = fields.IntegerField()
    reverse_count = fields.IntegerField()
    images = fields.ListField()
    processor = fields.ListField()
    images_time_stamp = fields.ListField()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def greeting():
    """ Welcomes user to image processor

    This function returns the following string: "Welcome to the image
    processor"

    Returns:
        welcome (string): "Welcome to the image processor"
    """

    welcome = "Welcome to the image processor"
    return welcome


@app.route("/data/<image_id>", methods=["GET"])
def getData(image_id):
    """
    This function returns all the stored information for a patient
    as a JSON dictionary

    Args:
        image_id (string): string specifying image name.

    Returns:
        dict_array (dict): stored information for specified image
    """

    u = User.objects.raw({"_id": image_id}).first()
    dict_array = {
                 }
    return jsonify(dict_array)


@app.route("/new_image", methods=["POST"])
def addimage():
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
    u = User(
             )
    logging.debug("Image {} was"
                  " successfully initialized".format(u.name))
    u.save()
    return u.name


if __name__ == "__main__":
    app.run(host="0.0.0.0")
