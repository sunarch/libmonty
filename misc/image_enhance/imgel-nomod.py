#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Image
import numpy

# Open the image file
src_image = Image.open("py_test.JPG")

# Attempt to ensure image is RGB
src_rgb = src_image.convert(mode="RGB")

# Create array of image using numpy
src_array = numpy.asarray(src_rgb)

# Modify array here


# Create image from array
final_image = Image.fromarray(src_array, "RGB")

# Save
final_image.save("py_test_out.jpg")
