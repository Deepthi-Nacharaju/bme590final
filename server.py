from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import base64
import io as io2
import numpy as np
from skimage import io as im
from skimage import io, exposure
from PIL import Image
import logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')

app = Flask(__name__)
connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")


class ImageDB(MongoModel):
    """

    This class initializes the stored data fields for the image processor
    MongoDB database.

    Attributes:
        patient_id (str): unique patient number.
        original (list): associated original image for each upload
        histogram_count (int): number of times histogram
            equalization was conducted.
        contrast_count (int): number of times contrast stretching
            was conducted.
        log_count (int): number of times log compression
            was conducted.
        reverse_count (int): number of times reverse video
            was conducted.
        images (list): list of original image and processed images.
        processor (list): list of completed processor actions.
        images_time_stamp (list): list of timestamps of completed
            processor actions.
        notes (list): extraneous notes provided by user.

    """
    patient_id = fields.CharField(primary_key=True)
    original = fields.ListField()
    histogram_count = fields.IntegerField()
    contrast_count = fields.IntegerField()
    log_count = fields.IntegerField()
    reverse_count = fields.IntegerField()
    images = fields.ListField()
    processor = fields.ListField()
    images_time_stamp = fields.ListField()
    notes = fields.ListField()


@app.route("/", methods=["GET"])
def greeting():
    """

    Returns "Welcome to the image processor"
    and confirms connection with the web server.

    Returns:
        (str): welcome: "Welcome to the image processor"

    """

    welcome = "Welcome to the image processor!"
    return jsonify(welcome), 200


def add_new_patient(patient_id, original_file):
    """

    Adds a new patient to the image processor
    and initializes image processor counts.

    Returns:
        (str): confirmation of new patient's
            initialization

    """
    patient = ImageDB(int(format(patient_id)),
                      histogram_count=0,
                      contrast_count=0,
                      log_count=0,
                      reverse_count=0)
    patient.save()
    try:
        patient.original.append(original_file)
    except AttributeError:
        patient.original = original_file
    patient.save()
    new_patient = 'New Patient Initialized with ID: ' + str(format(patient_id))
    return print(new_patient), 200


@app.route("/data/all/<patient_id>", methods=["GET"])
def get_all_data(patient_id):
    """

    Returns stored counts information for a patient
    as a JSON dictionary

    Args:
        patient_id (str): string specifying patient id.

    Returns:
        (dict): dict_array: dictionary of all stored data

    """
    try:
        u = ImageDB.objects.raw({"_id": str(patient_id)}).first()
        dict_array = {
            "original": u.original,
            "histogram_count": u.histogram_count,
            "contrast_count": u.contrast_count,
            "log_count": u.log_count,
            "reverse_count": u.reverse_count,
            "images": u.images,
            "processor": u.processor,
            "images_time_stamp": u.images_time_stamp,
            "notes": u.notes,
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    return jsonify(dict_array), 200


@app.route("/data/stack/<patient_id>", methods=["GET"])
def get_stack(patient_id):
    """

    Returns a list of all images processed for a
    specified patient ID

    Args:
        patient_id (str): usually patient mrn.

    Returns:
        (dict): dict_array: dictionary containing list of images.

    """
    try:
        u = ImageDB.objects.raw({"_id": str(format(patient_id))}).first()
        dict_array = {
            "images": u.images,
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    return jsonify(dict_array), 200


@app.route("/data/<patient_id>", methods=["GET"])
def get_data(patient_id):
    """

    Returns the stored image processing counts for a
    patient as a JSON dictionary

    Args:
        patient_id (str): string specifying patient id.

    Returns:
         (dict): dict_array: dictionary of image processor counts.

    """
    try:
        u = ImageDB.objects.raw({"_id": str(patient_id)}).first()
        dict_array = {
            "histogram_count": u.histogram_count,
            "contrast_count": u.contrast_count,
            "log_count": u.log_count,
            "reverse_count": u.reverse_count,
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    return jsonify(dict_array), 200


@app.route("/data/last/<patient_id>", methods=["GET"])
def get_last(patient_id):
    """

    Returns the original and most recent images in an image
    processing tree.

    Args:
        patient_id (str): string specifying patient id.

    Returns:
        (dict): dict_array: dictionary of images.

    """
    try:
        u = ImageDB.objects.raw({"_id": str(patient_id)}).first()
        dict_array = {
            "original": u.original[0],
            "last_process": u.images[-1],
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    return jsonify(dict_array), 200


@app.route("/new_image", methods=["POST"])
def new_image():
    """

    Receives a JSON request with an image and
    applies the specified image processing algorithm.

    Args:
        patient_id (str): specifies patient id.
        process_id (str): specifies type of algorithm.
        image_file (str): image as b64 string.

    Returns:
         (str): confirmation: upload confirmation of image

    """
    r = request.get_json()
    patient_id = r['patient_id']
    process_id = r['process_id']
    image_file_encoded = r['image_file']
    notes = r['notes']
    original = r['original']
    image_file = decode_b64_image(image_file_encoded)
    try:
        patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    except ImageDB.DoesNotExist:
        print('Could Not find user')
        new = add_new_patient(patient_id, image_file)
        logging.debug(new)
    if process_id is 1:
        processor = 'Histogram Equalization'
        patient.histogram_count += 1
        processed_image = histogram_equalization(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 2:
        processor = 'Contrast Switch'
        patient.contrast_count += 1
        processed_image = contrast_stretch(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 3:
        processor = 'Log Compression'
        patient.log_count += 1
        processed_image = log_compression(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 4:
        processor = 'Reverse Video'
        patient.reverse_count += 1
        processed_image = reverse_video(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 0:
        processor = 'Raw Image'
        processed_image = image_file
        logging.debug(processor)
    else:
        return jsonify('Not a valid ID')
    try:
        patient.original.append(original)
    except AttributeError:
        patient.original = original
    patient.save()
    out = encode_file_as_b64(processed_image)
    save_image(patient_id, processor, out, notes)
    return jsonify(out), 200


def save_image(patient_id, processor, image_file, notes):
    """

    This function updates the database by appending an image,
    processor type, timestamp, and notes for a specific patient_id.

    Args:
        patient_id (str): specifies patient id.
        processor (str): specifies type of algorithm.
        image_file (str): processed image file to be saved.
        notes (str): Any notes the user would like additionally saved.

    Returns:

    """
    patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    try:
        patient.images.append(image_file)
    except AttributeError:
        patient.images = image_file
    try:
        patient.images_time_stamp.append(datetime.datetime.now())
    except AttributeError:
        patient.images_time_stamp = datetime.datetime.now()
    try:
        patient.processor.append(processor)
    except AttributeError:
        patient.processor = processor
    try:
        patient.notes.append(notes)
    except AttributeError:
        patient.notes = notes
    patient.save()
    logging.debug('Patient saved')
    return


def decode_b64_image(base64_string):
    """

    This function takes in a base64 string and decodes it into an
    image array.

    Args:
        base64_string (str): specifies base64
            representation of an image.

    Returns:
        PIL image object (array): reconstructed_image

    """
    temp = open("temporary.png", "wb")
    temp.write(base64.b64decode(base64_string))
    temp.close()
    reconstructed_image = im.imread("temporary.png")
    return reconstructed_image


def encode_file_as_b64(image_array):
    """

    This function takes in an image array and encodes it into its
    base64 representation.

    Args:
        image_array : PIL image

    Returns:
        (str): image_string: base64 representation of image

    """
    image = Image.fromarray(image_array)
    buffer = io2.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    image_string = base64.b64encode(image_bytes).decode("utf-8")
    #    with open(image_path, "rb") as image_file:
    #        return base64.b64encode(image_file.read())
    return image_string


def make_gray(pil_image):
    """

    This function takes in an image array and converts it to
    gray scale.

    Args:
        PIL_array : image array

    Returns:
        PIL image object (array) : processed_image: gray scale image

    """
    image = Image.fromarray(pil_image)
    gray_scale = image.convert('LA')
    # gray = np.array(gray_scale)
    processed_image = gray_scale
    return processed_image


def is_gray(pil_image):
    """

    This function takes in an image array and determines
    if it's in gray scale. Adapted from: joaoricardo000
    on stackoverflow.com

    Args:
        PIL_array : image array

    Returns:
        (bool): gray scale: if the image is gray scale.

    """

    image = Image.fromarray(pil_image)
    imageRGB = image.convert('RGB')
    w, h = imageRGB.size
    for i in range(w):
        for j in range(h):
            r, g, b = imageRGB.getpixel((i, j))
            if r != g != b:
                return False
    return True


def histogram_equalization(pil_image):
    """

    This function takes in an image array, determines if it's gray scale
    (and converts if it isn't), and performs histogram equalization.

    Args:
        pil_image : image array

    Returns:
        PIL image object (array): processed_image: image array with
            histogram equalization applied.

    """
    if not is_gray(pil_image):
        gray = make_gray(pil_image)
        gray.save('temp.png')
        gray = io.imread('temp.png')
    else:
        gray = pil_image
    equalized = exposure.equalize_hist(gray)
    normalized = 255 * equalized
    processed_image = normalized.astype('uint8')
    return processed_image


def contrast_stretch(pil_image):
    """

    This function takes in an image array and performs
    contrast stretching.

    Args:
        pil_image : image array

    Returns:
        PIL image object (array): processed_image: image array
            with contrast stretching applied.

    """
    p2 = np.percentile(pil_image, 2)
    p98 = np.percentile(pil_image, 98)
    rescaled_image = exposure.rescale_intensity(pil_image, in_range=(p2, p98))
    processed_image = rescaled_image
    return processed_image


def log_compression(pil_image):
    """

    This function takes in an image array and performs
    log compression.
    Adapted from: https://homepages.inf.ed.ac.uk/rbf/HIPR2/pixlog.htm

    Args:
        pil_image : image array

    Returns:
        PIL image object (array): processed_image: image array with
            log compression applied.

    """
    # Adapted from:
    # https://homepages.inf.ed.ac.uk/rbf/HIPR2/pixlog.htm
    c = 255 / (np.log10(1 + np.amax(pil_image)))
    for pixel in np.nditer(pil_image, op_flags=['readwrite']):
        pixel[...] = c * np.log10(1 + pixel)
    processed_image = pil_image.astype('uint8')
    return processed_image


def reverse_video(pil_image):
    """

    This function takes in an image array and performs
    reverse video by subtracting each pixel from 255.

    Args:
        pil_image : image array

    Returns:
        PIL image object (array): processed_image: image array with
            reverse video applied.

    """
    for pixel in np.nditer(pil_image, op_flags=['readwrite']):
        pixel[...] = 255 - pixel
    processed_image = pil_image.astype('uint8')
    return processed_image


if __name__ == "__main__":
    connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
    # app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
