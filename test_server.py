import pytest
from server import encode_file_as_b64
from server import decode_b64_image
from server import reverse_video
import base64
import io
from skimage import io as io2
import matplotlib.image as mpimg
import numpy as np
from PIL import Image


def test_validate_image():
    assert True


def test_reverse_video():
    correct = io2.imread('testreversevideo.png')
    dog = io2.imread('Dogs.jpg')
    dog_reverse = reverse_video(dog)
    assert np.array_equal(dog_reverse, correct)


def test_decode_b64_image():
    dog = io2.imread('Dogs.jpg')
    correctdogb64 = open('dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    dog_decoded = decode_b64_image(correctb64)
    assert np.array_equal(dog, dog_decoded)


def test_encode_file_as_b64():

    dog = io2.imread('Dogs.jpg')
    b64 = encode_file_as_b64(dog)
    correctdogb64 = open('dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    assert b64 == correctb64
