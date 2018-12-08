import pytest
from server import encode_file_as_b64
from server import decode_b64_image
import base64
import io
import matplotlib.image as mpimg


def test_validate_image():
    assert True


#def test_decode_b64_image():
#    encoded = encode_file_as_b64('Dogs.jpg')
#    image_bytes = base64.b64decode(encoded)
#    image_bytes2 = decode_b64_image(encoded)
#    assert image_bytes == image_bytes2


def test_encode_file_as_b64():
    encoded = encode_file_as_b64('Dogs.jpg')
    with open('Dogs.jpg', "rb") as image_file:
        encoded2 = base64.b64encode(image_file.read())
    assert encoded == encoded2
