import base64
from matplotlib import pyplot as plt
import io
from PIL import Image, ImageOps


def encode_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def decode_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = Image.open(image_buf, mode='r')
    # plt.imshow(i, interpolation='nearest')
    # plt.show()
    return i  # This is an image object in Pillow in <JpegImageFile>


def PIL_to_mode(PIL_image, mode):  # returns a converted copy of an image to desired mode
    out = PIL_image.convert(mode=mode)
    # plt.imshow(out, interpolation='nearest')
    # plt.show()
    return out


def is_threeband(PIL_image):
    raster = PIL_image.getbands()
    if len(raster) == 1:
        return False
    if 1 < len(raster) <= 3:
        return True
    if len(raster) > 3:
        return False


def histogram_equalization(image_obj):  # Pil image
    im = ImageOps.equalize(image_obj, mask=None)
    # plt.imshow(im)
    # plt.show()
    return im


def normalizeRed(intensity):  # method to process the red band of the image
    iI = intensity
    minI = 86
    maxI = 230
    minO = 0
    maxO = 255
    iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
    return iO


def normalizeGreen(intensity):  # method to process the green band of the image
    iI = intensity
    minI = 90
    maxI = 225
    minO = 0
    maxO = 255
    iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
    return iO


def normalizeBlue(intensity):
    iI = intensity
    minI = 100
    maxI = 210
    minO = 0
    maxO = 255
    iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
    return iO


def contrast_stretch(image_obj):
    # if is_threeband(image_obj) == False:
    if is_threeband(image_obj) == True:  # if image is RGB
        multiBands = image_obj.split()  # split the R, G, B bands from the image
        normalizedR = multiBands[0].point(normalizeRed)
        normalizedG = multiBands[1].point(normalizeGreen)
        normalizedB = multiBands[2].point(normalizeBlue)
        normalized_image = Image.merge("RGB", (normalizedR, normalizedG, normalizedB))
        normalized_image.show()
        print(type(normalized_image))
        return normalized_image


if __name__ == "__main__":
    enc = encode_file_as_b64("Dogs.jpg")
    dec = decode_b64_image(enc)
