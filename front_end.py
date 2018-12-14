import base64
import io
import matplotlib.image as mpimg
# Stuff for color intensity histogram
import matplotlib.pyplot as plt
from PIL import Image
from skimage import io as im


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
    temp = open("temporary.png", "wb")
    temp.write(image_bytes)
    temp.close()
    reconstructed_image = im.imread("temporary.png")
    return reconstructed_image


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
    fig = plt.figure(frameon=False)
    plt.hist(r_list, bins=20, alpha=0.5, color='red')
    plt.hist(g_list, bins=20, alpha=0.5, color='green')
    plt.hist(b_list, bins=20, alpha=0.5, color='blue')
    plt.ylabel('Frequency')
    plt.xlabel('RGB')
    plt.savefig(save_name, bbox_inches='tight', pad_inches=0)
    return r_list, g_list, b_list


if __name__ == "__main__":
    get_histogram_values('Original_Hist.jpg')
