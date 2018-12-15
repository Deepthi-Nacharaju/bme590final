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
from zipfile import ZipFile

# logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')

app = Flask(__name__)
connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")


class ImageDB(MongoModel):
    """This class initializes the stored data fields for the image processor
    MongoDB database.

    Attributes:
        patient_id (str): unique patient mrn.
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
    histogram_count = fields.ListField()
    contrast_count = fields.ListField()
    log_count = fields.ListField()
    reverse_count = fields.ListField()
    images = fields.ListField()
    processor = fields.ListField()
    images_time_stamp = fields.ListField()
    notes = fields.ListField()


@app.route("/", methods=["GET"])
def greeting():
    """ Welcomes user to image processor

    This function returns "Welcome to the image processor"
    and confirms connection with the web server.

    Returns:
        welcome (str): "Welcome to the image processor"

    """

    welcome = "Welcome to the image processor!"
    return jsonify(welcome)


def add_new_patient(patient_id, original_file, length):
    """ Adds new patient to image processor

    Returns:
        new_patient (str): confirmation of new patient's
            initialization

    """
    count_list = [0] * length
    patient = ImageDB(int(format(patient_id)),
                      histogram_count=count_list,
                      contrast_count=count_list,
                      log_count=count_list,
                      reverse_count=count_list)
    patient.save()
    try:
        patient.original.append(original_file)
    except AttributeError:
        patient.original = original_file
    patient.save()
    new_patient = 'New Patient Initialized with ID: ' + str(format(patient_id))
    return print(new_patient)


@app.route("/data/all/<patient_id>", methods=["GET"])
def get_all_data(patient_id):
    """Returns stored counts information for a patient
    as a JSON dictionary

    Args:
        patient_id (str): string specifying patient id.

    Returns:
         dict_array (dict): dictionary of all stored data

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
    return jsonify(dict_array)


@app.route("/data/stack/<patient_id>", methods=["GET"])
def get_stack(patient_id):
    """

    :param patient_id: usually patient mrn
    :return: json dictionary of all image layers
    """
    try:
        u = ImageDB.objects.raw({"_id": str(format(patient_id))}).first()
        dict_array = {
            "images": u.images,
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    return jsonify(dict_array)


@app.route("/data/<patient_id>", methods=["GET"])
def get_data(patient_id):
    """Returns all the stored information for a patient
    as a JSON dictionary

    Args:
        patient_id (str): string specifying patient id.

    Returns:
         dict_array (dict): dictionary of all stored data

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
    return jsonify(dict_array)


@app.route("/data/last/<patient_id>", methods=["GET"])
def get_last(patient_id):
    """Returns all the stored information for a patient
    as a JSON dictionary

    Args:
        patient_id (str): string specifying patient id.

    Returns:
         dict_array (dict): dictionary of all stored data

    """
    try:
        u = ImageDB.objects.raw({"_id": str(patient_id)}).first()
        dict_array = {
            "original": u.original,
            "last_process": u.images[-1],
        }
    except ImageDB.DoesNotExist:
        dict_array = 'DNE'
    except IndexError:
        dict_array = 'DNE'
    return jsonify(dict_array)


@app.route("/new_image", methods=["POST"])
def new_image():
    """This function receives a JSON request with
     an image and applies the specified image
     processing algorithm.

    Args:
        patient_id (str): specifies patient id.
        process_id (str): specifies type of algorithm
        image_file (str): image as b64 string

    Returns:
         confirmation (str): upload confirmation of image

    """
    r = request.get_json()
    patient_id = r['patient_id']
    process_id = r['process_id']
    image_file_encoded = r['image_file']
    notes = r['notes']
    original = r['original']
    try:
        index = r['index']
        image_file = decode_b64_image(image_file_encoded[index])
    except KeyError:
        image_file = decode_b64_image(image_file_encoded)
    try:
        patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    except ImageDB.DoesNotExist:
        print('Could Not find user')
        length = len(original)
        new = add_new_patient(patient_id, image_file, length)
        logging.debug(new)
    if process_id is 1:
        processor = 'Histogram Equalization'
        if index:
            count = patient.histogram_count
            count[index] += 1
            patient.histogram_count = count
        else:
            patient.histogram_count += 1
        processed_image = histogram_equalization(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 2:
        processor = 'Contrast Switch'
        if index:
            count = patient.contrast_count
            count[index] += 1
            patient.contrast_count = count
        else:
            patient.contrast_count += 1
        processed_image = contrast_stretch(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 3:
        processor = 'Log Compression'
        if index:
            count = patient.log_count
            count[index] += 1
            patient.log_count = count
        else:
            patient.log_count += 1
        processed_image = log_compression(image_file)
        logging.debug(processor + ' was conducted')
    elif process_id is 4:
        processor = 'Reverse Video'
        if index:
            count = patient.reverse_count
            count[index] += 1
            patient.reverse_count = count
        else:
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
    if index:
        save_image(patient_id, processor, out, notes,
                   index, image_file_encoded)
    else:
        save_image(patient_id, processor, out, notes)
    return jsonify(out)


def save_image(patient_id, processor, image_file, notes,
               index=None, image_list=None):
    """

    :param patient_id: Usually mrn number
    :param processor: Type of processor applied to original image
    :param image_file: Processed Image file to be saved
    :param original: Original Image file to be saved
    :param notes: Any notes the user would like additionally saved
    :return:
    """
    patient = ImageDB.objects.raw({"_id": str(patient_id)}).first()
    if not index:
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
    else:
        image_list[index] = image_file
        try:
            patient.images.append(image_list)
        except AttributeError:
            patient.images = image_list
        time_stamp_array = [0] * len(image_list)
        time_stamp_array[index] = datetime.datetime.now()
        try:
            patient.images_time_stamp.append(time_stamp_array)
        except AttributeError:
            patient.images_time_stamp = time_stamp_array
        processor_array = [''] * len(image_list)
        processor_array[index] = processor
        try:
            patient.processor.append(processor_array)
        except AttributeError:
            patient.processor = processor_array
        notes_array = [''] * len(image_list)
        notes_array[index] = notes
        try:
            patient.notes.append(notes_array)
        except AttributeError:
            patient.notes = notes_array
    patient.save()
    return


def decode_b64_image(base64_string):
    """
    :param base64_string:
    :return reconstructed_image: PIL image
    """
    temp = open("temporary.png", "wb")
    temp.write(base64.b64decode(base64_string))
    temp.close()
    reconstructed_image = im.imread("temporary.png")
    return reconstructed_image


def encode_file_as_b64(image_array):
    """

    :param image_array: PIL Image
    :return: base64_string
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

    :param pil_image: PIL Image to be processed
    :return: gray scale image
    """
    image = Image.fromarray(pil_image)
    gray_scale = image.convert('LA')
    # gray = np.array(gray_scale)
    processed_image = gray_scale
    return processed_image


def is_gray(pil_image):
    """

    :param pil_image: PIL image to be processed
    :return: if image is grayscale or not
    """
    # https://stackoverflow.com/questions
    # /23660929/how-to-check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli
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

    :param pil_image: PIL Image to be processed
    :return: processed image that has histogram equalization
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

    :param pil_image: PIL Image to be processed
    :return: Image that has been contrast stretched
    """
    p2 = np.percentile(pil_image, 2)
    p98 = np.percentile(pil_image, 98)
    rescaled_image = exposure.rescale_intensity(pil_image, in_range=(p2, p98))
    processed_image = rescaled_image
    return processed_image


def log_compression(pil_image):
    """

    :param pil_image: PIL image to be processed
    :return: Image that has been log compressed
    """
    # Adapted from:
    # https://homepages.inf.ed.ac.uk/rbf/HIPR2/pixlog.htm
    c = 255 / (np.log10(1 + np.amax(pil_image)))
    for pixel in np.nditer(pil_image, op_flags=['readwrite']):
        pixel[...] = c * np.log10(1 + pixel)
    processed_image = pil_image.astype('uint8')
    return processed_image


def reverse_video(pil_image):
    """This function reverses the colors in an image

    Args:
        pil_image (array): PIL image object

    Returns:
        processed_image (array): PIL image object

    """
    for pixel in np.nditer(pil_image, op_flags=['readwrite']):
        pixel[...] = 255 - pixel
    processed_image = pil_image.astype('uint8')
    return processed_image


def read_zip(filename):
    """This function opens each file inside a zip file.

    :param filename (string): .zip file name
    :return: extracted files in current directory
    """
    with Zipfile(fiename, 'r') as zip:
        zip.printdir()
        zip.extractall()


def write_zip(url):
    """ This function downloads a ZIP file via URL
    and extract its contents in memory
    :param: url (str): url
    :return: (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
        for zipinfo in zip.infolist():
            with zip.open(zipinfo) as file:
                yield zipinfo.filename, file


if __name__ == "__main__":
    connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
    app.run(host="127.0.0.1")
