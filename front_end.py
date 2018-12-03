from PIL import Image, ImageFilter
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def encode_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


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
    out = read_jpg('Dogs.jpg')
