#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# import 'sys' and 'getopt' for command-line argument passing
import sys
import getopt
# import 'Image' from the PIL and 'numpy' for image processing and calculations
from PIL import Image
import numpy


# basic functions ##############################################################

def arithmetic_mean_int(arg_num_list):
    num_list = arg_num_list
    num_count = len(num_list)
    num_sum = 0
    for i1 in range(num_count):
        num_sum += num_list[i1]
    return int(num_sum / num_count)


def is_even(arg_num):
    if arg_num % 2 == 0:
        return True
    else:
        return False


def is_odd(arg_num):
    if arg_num % 2 == 1:
        return True
    else:
        return False


# global variables #############################################################

src_array = None
src_image_height = 0
src_image_width = 0
final_image_height = 0
final_image_width = 0
final_array = None


# preparation functions ########################################################

def double_pixels_1():
    # insert a black pixel between every source pixel
    # Required by filling function two_point_filling_1()
    # Required by filling function four_point_filling_1()

    # defining scope for global variables
    global src_array
    global src_image_height
    global src_image_width
    global final_image_height
    global final_image_width
    global final_array

    # define new image target dimensions
    final_image_height = 2 * src_image_height - 1
    final_image_width = 2 * src_image_width - 1

    # create array for new image grid and fill it up with zeros
    # it is important that the data type is uint8 (unsigned integer 8) or the output will be scrambled
    final_array = numpy.zeros((final_image_height, final_image_width, 3), dtype=numpy.uint8)

    # Runthrough 1: filling the new grid with source pixels and black pixels
    for i1 in range(final_image_height):
        # odd vertical pixels
        if is_odd(i1 + 1):
            for i2 in range(final_image_width):
                # odd horizontal pixels
                if is_odd(i2 + 1):
                    for i3 in range(3):
                        final_array[i1][i2][i3] = src_array[(i1-1)/2][(i2-1)/2][i3]
                else:
                    for i3 in range(3):
                        final_array[i1][i2][i3] = 0
        else:
            for i2 in range(final_image_width):
                for i3 in range(3):
                    final_array[i1][i2][i3] = 0

    # Debugging new image dimensions
    print('Final image height:', len(final_array))
    print('Final image width:', len(final_array[1]))


# filling functions ############################################################

def two_point_filling_1():
    # 1) horizontal 2-point: pos_5 = arithmetic_mean_int((pos_4, pos_6)) where both are original pixels
    # 2) vertical 2-point: pos_5 = arithmetic_mean_int((pos_8, pos_2)) where both are original pixels
    # 3) diagonal 4-point: pos_5 = arithmetic_mean_int((pos_7, pos_9, pos_1, pos_2)) where all 4 art original pixels

    # defining scope for global variables
    global src_array
    global src_image_height
    global src_image_width
    global final_image_height
    global final_image_width
    global final_array

    # Requires preparation function double_pixels_1()
    double_pixels_1()

    # Runthrough 1: estimating new pixels with 2 horizontal source pixel neighbors
    for i1 in range(final_image_height):
        # odd vertical pixels
        if is_odd(i1 + 1):
            for i2 in range(final_image_width):
                # even horizontal pixels
                if is_even(i2 + 1):
                    for i3 in range(3):
                        # horizontal 2-point average
                        final_array[i1][i2][i3] = arithmetic_mean_int((final_array[i1][i2-1][i3],final_array[i1][i2+1][i3]))

    # Runthrough 2: estimating new pixels with 2 vertical source pixel neighbors
    for i1 in range(final_image_height):
        # even vertical pixels
        if is_even(i1 + 1):
            for i2 in range(final_image_width):
                # odd horizontal pixels
                if is_odd(i2 + 1):
                    for i3 in range(3):
                        # vertical 2-point average
                        final_array[i1][i2][i3] = arithmetic_mean_int((final_array[i1-1][i2][i3],final_array[i1+1][i2][i3]))

    # Runthrough 3: estimating new pixels with only diagonal source pixel neighbors
    for i1 in range(final_image_height):
        # even vertical pixels
        if is_even(i1 + 1):
            for i2 in range(final_image_width):
                # even horizontal pixels
                if is_even(i2 + 1):
                    for i3 in range(3):
                        top_left = final_array[i1-1][i2-1][i3]
                        top_right = final_array[i1-1][i2+1][i3]
                        bottom_left = final_array[i1+1][i2-1][i3]
                        bottom_right = final_array[i1+1][i2+1][i3]
                        # diagonal 4-point average
                        final_array[i1][i2][i3] = arithmetic_mean_int((top_left,top_right,bottom_left,bottom_right))

    return True


def four_point_filling_1():
    # 1) diagonal 4-point: pos_5 =
    #   arithmetic_mean_int((pos_7, pos_9, pos_1, pos_2)) where all 4 are original pixels
    # 2) horizontal 4-point: pos_5 =
    #   arithmetic_mean_int((pos_8, pos_2, pos_4, pos_6)) where pos_4 and pos_6 are original pixels
    # 3) vertical 4-point: pos_5 =
    #   arithmetic_mean_int((pos_8, pos_2, pos_4, pos_6)) where pos_8 and pos_2 are original pixels

    # defining scope for global variables
    global src_array
    global src_image_height
    global src_image_width
    global final_image_height
    global final_image_width
    global final_array

    # Requires preparation function double_pixels_1()
    double_pixels_1()

    return True


# main function ################################################################

def main(argv):

    # defining scope for global variables
    global src_array
    global src_image_height
    global src_image_width
    global final_image_height
    global final_image_width
    global final_array

    # function-scoped variables for command arguments
    inputfile = ''
    outputfile = ''

    # define command argument possibilities
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        print('Usage: \'./imgel.py -i <inputfile> -o <outputfile>\'')
        sys.exit(2)

    # define actions based on command argument switches
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: \'./imgel.py -i <inputfile> -o <outputfile>\'')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    # debug variable values gotten out of arguments
    print('Input file:', inputfile)
    print('Output file:', outputfile)

    # get source file name and target file name from args
    src_file = str(inputfile)
    target_file = str(outputfile)

    # [ORIGINAL:] Open the image file
    src_image = Image.open(src_file)

    # [ORIGINAL:] Attempt to ensure image is RGB
    src_rgb = src_image.convert(mode='RGB')

    # [ORIGINAL:] Create array of image using numpy
    src_array = numpy.asarray(src_rgb)

    # save values of image array length for easier referencing
    src_image_height = len(src_array)
    src_image_width = len(src_array[1])

    # debug source image dimension values
    print('Source image height:', src_image_height)
    print('Source image width:', src_image_width)

    # [ORIGINAL:] Modify array here

    # execute modification functions
    # not optioned yet, default is present
    two_point_filling_1()

    # [ORIGINAL:] Create image from array
    final_image = Image.fromarray(final_array, 'RGB')

    # [ORIGINAL:] Save
    final_image.save(target_file)


# start program ################################################################

if __name__ == '__main__':
    main(sys.argv[1:])

# END ##########################################################################
