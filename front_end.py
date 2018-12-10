from PIL import Image, ImageFilter
import base64
import io
import requests
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import PyQt5
# Stuff for color intensity histogram
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import colorsys
from PIL import Image


def encode_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        en64 = base64.b64encode(image_file.read())
        en64 = en64.decode("utf-8")
        return en64


def decode_b64_image(base64_string, save_name):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.savefig(save_name)

# def decode_b64_image(base64_string):
#     """
#     :param base64_string:
#     :return reconstructed_image: PIL image
#     """
#     from skimage import io as im
#     temp = open("temporary.png", "wb")
#     temp.write(base64.b64decode(base64_string))
#     temp.close()
#     reconstructed_image = im.imread("temporary.png")
# #    image_bytes = base64.b64decode(base64_string)
# #    image_buf = io.BytesIO(image_bytes)
# #    i = mpimg.imread(image_buf, format='JPG')
# #    plt.imshow(i, interpolation='nearest')
# #    plt.show()
#     return reconstructed_image
#
#
# def encode_file_as_b64(image_array):
#     image = Image.fromarray(image_array)
#     buffer = io.BytesIO()
#     image.save(buffer, format="JPEG")
#     image_bytes = buffer.getvalue()
#     image_string = base64.b64encode(image_bytes.decode("utf-8"))
# #    with open(image_path, "rb") as image_file:
# #        return base64.b64encode(image_file.read())
#     return image_string

def read_jpg(pic_str):
    with open(pic_str, 'rb') as pic:
        pic_data = pic.read()
        pic_data = str(pic_data)
    return pic_data


def get_histogram_values(image_name, save_name):
    # (1) Import the file to be analyzed!
    img_file = Image.open(image_name)
    img = img_file.load()

    # (2) Get image width & height in pixels
    [xs, ys] = img_file.size
    max_intensity = 100
    hues = {}
    r_list = []
    g_list = []
    b_list = []

    # (3) Examine each pixel in the image file
    for x in range(0, xs):
        for y in range(0, ys):
            # (4)  Get the RGB color of the pixel
            [r, g, b] = img[x, y]

            # (5)  Normalize pixel color values
            r /= 255.0
            g /= 255.0
            b /= 255.0
            r_list.append(r)
            g_list.append(g)
            b_list.append(b)

    # (9)   Plot the graph!
    fig = plt.figure()
    plt.hist(r_list, bins=20, alpha=0.5, color='red')
    plt.hist(g_list, bins=20, alpha=0.5, color='green')
    plt.hist(b_list, bins=20, alpha=0.5, color='blue')
    plt.ylabel('Frequency')
    plt.xlabel('RGB')
    plt.savefig(save_name)
    return

if __name__ == "__main__":
    get_histogram_values('Original_Hist.jpg')
    # server = "http://127.0.0.1:5000/"
    # r = requests.get(server)
    # print(r.json())
    # server = "http://127.0.0.1:5000/new_patient"
    # post_dict = {'patient_id': 1}
    # r = requests.post(server, json=post_dict)
    # print(r.json())
    # post_dict = {'patient_id': 2}
    # r = requests.post(server, json=post_dict)
    # p2_image = encode_file_as_b64('Dogs.jpg')
    # server = "http://127.0.0.1:5000/new_image"
    # post_dict = {'patient_id': 2,
    #              'process_id': 0,
    #              'image_file': p2_image}
    # r = requests.post(server, json=post_dict)
    # print(r.json())
    # server = "http://127.0.0.1:5000/data/2"
    # r = requests.get(server)
    # print(r.json())
