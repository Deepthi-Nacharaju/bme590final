from front_end import decode_b64_image
from front_end import encode_file_as_b64
from front_end import read_jpg
from front_end import get_histogram_values
import base64
import io
from skimage import io as io2
import matplotlib.image as mpimg
import numpy as np
from PIL import Image


def test_decode_b64_image():
    dog = io2.imread('testing_files/Dogs.png')
    correctdogb64 = open('testing_files/dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    dog_decoded = decode_b64_image(correctb64, 'temp.png')
    assert np.array_equal(dog, dog_decoded)


def test_encode_file_as_b64():
    b64 = encode_file_as_b64('testing_files/Dogs.png')
    correctdogb64 = open('testing_files/dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    assert b64 == correctb64


def test_read_jpg():
    data = read_jpg('testing_files/Dogs.jpg')
    correct_jpg = open('testing_files/jpg_read.txt')
    correct_jpg_data = correct_jpg.read()
    assert correct_jpg_data == data


def test_get_histogram_values():
    r, g, b = get_histogram_values('testing_files/Dogs.png', 'temp.png')
    correct = open('testing_files/test_histogram_values_R.txt', "r")
    correct_r = correct.read()
    correct = open('testing_files/test_histogram_values_G.txt', "r")
    correct_g = correct.read()
    correct = open('testing_files/test_histogram_values_B.txt', "r")
    correct_b = correct.read()
    assert str(r) == correct_r
    assert str(g) == correct_g
    assert str(b) == correct_b
