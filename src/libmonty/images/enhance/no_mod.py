#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Image open and save without modification
"""

# imports: library
import numpy
from PIL import Image


# Open the image file
src_image: Image = Image.open('py_test.JPG')

# Attempt to ensure image is RGB
src_rgb: Image = src_image.convert(mode='RGB')

# Create array of image using numpy
src_array: numpy.ndarray = numpy.asarray(src_rgb)

# Modify array here


# Create image from array
final_image: Image = Image.fromarray(src_array, 'RGB')

# Save
final_image.save('py_test_out.jpg')
