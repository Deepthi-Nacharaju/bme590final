import pytest
from server import encode_file_as_b64
from server import decode_b64_image
from server import reverse_video
from server import histogram_equalization
from server import contrast_stretch
from server import log_compression
from server import make_gray
import base64
import io
from skimage import io as io2
import matplotlib.image as mpimg
import numpy as np
from PIL import Image


def test_validate_image():
    assert True


# def test_make_gray():
#    correct = io2.imread('testing_files/testmakegray.png')
#    dog = io2.imread('testing_files/Dogs.jpg')
#    dog_gray = make_gray(dog)
    #    dog_gray = np.transpose(dog_gray, (2, 0, 1))
#    assert np.array_equal(dog_gray, correct)


def test_log_compression():
    correct = io2.imread('testing_files/testlogcompression.png')
    dog = io2.imread('testing_files/Dogs.jpg')
    dog_log_compression = log_compression(dog)
    assert np.array_equal(dog_log_compression, correct)


def test_contrast_stretch():
    correct = io2.imread('testing_files/testcontraststretch.png')
    dog = io2.imread('testing_files/Dogs.jpg')
    dog_contrast_stretch = contrast_stretch(dog)
    assert np.array_equal(dog_contrast_stretch, correct)


def test_histogram_equalization():
    correct = io2.imread('testing_files/testhistogramequalization.png')
    dog = io2.imread('testing_files/Dogs.jpg')
    dog_equalized = histogram_equalization(dog)
    assert np.array_equal(dog_equalized, correct)


def test_reverse_video():
    correct = io2.imread('testing_files/testreversevideo.png')
    dog = io2.imread('testing_files/Dogs.jpg')
    dog_reverse = reverse_video(dog)
    assert np.array_equal(dog_reverse, correct)


def test_decode_b64_image():
    dog = io2.imread('testing_files/Dogs.jpg')
    correctdogb64 = open('testing_files/dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    dog_decoded = decode_b64_image(correctb64)
    assert np.array_equal(dog, dog_decoded)


def test_encode_file_as_b64():
    dog = io2.imread('testing_files/Dogs.jpg')
    b64 = encode_file_as_b64(dog)
    correctdogb64 = open('testing_files/dogb64.txt', "r")
    correctb64 = correctdogb64.read()
    assert b64 == correctb64
