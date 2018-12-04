from PIL import Image, ImageFilter
import base64
import io
import requests
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def encode_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        en64 = base64.b64encode(image_file.read())
        return str(en64)


def decode_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()


def read_jpg(pic_str):
    with open(pic_str, 'rb') as pic:
        pic_data = pic.read()
        pic_data = str(pic_data)
    return pic_data


if __name__ == "__main__":
    server = "http://127.0.0.1:5000/"
    r = requests.get(server)
    print(r.json())
    server = "http://127.0.0.1:5000/new_patient"
    post_dict = {'patient_id': 1}
    r = requests.post(server, json=post_dict)
    print(r.json())
    post_dict = {'patient_id': 2}
    r = requests.post(server, json=post_dict)
    p2_image = encode_file_as_b64('Dogs.jpg')
    server = "http://127.0.0.1:5000/process"
    post_dict = {'patient_id': 2,
                 'process_id': 0,
                 'image_file': p2_image}
    r = requests.post(server, json=post_dict)
    print(r.json())
    #server = "http://127.0.0.1:5000/data/2"
    #r = requests.get(server)
    #print(r.json())

