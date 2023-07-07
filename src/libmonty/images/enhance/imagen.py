#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Image enhance
"""

# library
from argparse import ArgumentParser, Namespace
import os.path
from typing import Iterable, Sized

# imports: requirements
import numpy
from PIL import Image
from tqdm import tqdm

# imports: project
from libmonty.environment.arguments import type_file_path


def arithmetic_mean(numbers: Iterable[int] and Sized) -> int:
    """Arithmetic mean"""

    return int(sum(numbers) / len(numbers))


def is_even(number: int) -> bool:
    """Is even?"""

    return number % 2 == 0


def is_odd(number: int) -> bool:
    """Is odd?"""

    return number % 2 == 1


def double_pixels_1(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Double pixels v1

    Insert a black pixel between every source pixel
    """

    target_image_height = 2 * len(pixel_matrix) - 1
    target_image_width = 2 * len(pixel_matrix[1]) - 1

    print('Doubling pixels')

    # create array for new image grid and fill it up with zeros
    # it is important that the data type is uint8 (unsigned integer 8) or the output will be scrambled
    new_pixel_matrix = numpy.zeros((target_image_height, target_image_width, 3), dtype=numpy.uint8)

    # filling the new grid with source pixels and black pixels
    for row in tqdm(range(target_image_height), 'Rows', target_image_height):
        # odd vertical pixels
        if is_odd(row + 1):
            for column in range(target_image_width):
                # odd horizontal pixels
                if is_odd(column + 1):
                    for value_index in range(3):
                        original_row = int((row - 1) / 2)
                        original_column = int((column - 1) / 2)
                        new_pixel_matrix[row][column][value_index] = pixel_matrix[original_row][original_column][value_index]
                else:
                    for value_index in range(3):
                        new_pixel_matrix[row][column][value_index] = 0
        else:
            for column in range(target_image_width):
                for value_index in range(3):
                    new_pixel_matrix[row][column][value_index] = 0

    print('Extended image height:', len(new_pixel_matrix))
    print('Extended image width: ', len(new_pixel_matrix[0]))

    return new_pixel_matrix


def two_point_filling_1(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Two point filling v1"""

    pixel_matrix = double_pixels_1(pixel_matrix)

    # Runthrough 1: estimating new pixels with 2 horizontal source pixel neighbors
    pixel_matrix = two_point_filling_1_horizontal(pixel_matrix)
    # Runthrough 2: estimating new pixels with 2 vertical source pixel neighbors
    pixel_matrix = two_point_filling_1_vertical(pixel_matrix)
    # Runthrough 3: estimating new pixels with only diagonal source pixel neighbors
    pixel_matrix = two_point_filling_1_diagonal(pixel_matrix)

    return pixel_matrix


def two_point_filling_1_horizontal(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Two point filling v1 - horizontal"""

    # horizontal 2-point:
    # pos_5 = arithmetic_mean_int((pos_4, pos_6)) where both are original pixels

    image_height = len(pixel_matrix)
    image_width = len(pixel_matrix[0])

    print('Two point filling - horizontal')

    for row in tqdm(range(image_height), 'Rows', image_height):
        # odd vertical pixels
        if is_odd(row + 1):
            for column in range(image_width):
                # even horizontal pixels
                if is_even(column + 1):
                    for value_index in range(3):
                        # horizontal 2-point average
                        value_left = pixel_matrix[row][column - 1][value_index]
                        value_right = pixel_matrix[row][column + 1][value_index]
                        pixel_matrix[row][column][value_index] = arithmetic_mean((value_left, value_right))

    return pixel_matrix


def two_point_filling_1_vertical(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Two point filling v1 - vertical"""

    # vertical 2-point:
    # pos_5 = arithmetic_mean_int((pos_8, pos_2)) where both are original pixels

    image_height = len(pixel_matrix)
    image_width = len(pixel_matrix[0])

    print('Two point filling - vertical')

    for row in tqdm(range(image_height), 'Rows', image_height):
        # even vertical pixels
        if is_even(row + 1):
            for column in range(image_width):
                # odd horizontal pixels
                if is_odd(column + 1):
                    for value_index in range(3):
                        # vertical 2-point average
                        value_above = pixel_matrix[row - 1][column][value_index]
                        value_below = pixel_matrix[row + 1][column][value_index]
                        pixel_matrix[row][column][value_index] = arithmetic_mean((value_above, value_below))

    return pixel_matrix


def two_point_filling_1_diagonal(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Two point filling v1 - diagonal"""

    # diagonal 4-point:
    # pos_5 = arithmetic_mean_int((pos_7, pos_9, pos_1, pos_2)) where all 4 are original pixels

    image_height = len(pixel_matrix)
    image_width = len(pixel_matrix[1])

    print('Two point filling - vertical')

    for row in tqdm(range(image_height), 'Rows', image_height):
        # even vertical pixels
        if is_even(row + 1):
            for column in range(image_width):
                # even horizontal pixels
                if is_even(column + 1):
                    for value_index in range(3):
                        top_left = pixel_matrix[row-1][column-1][value_index]
                        top_right = pixel_matrix[row-1][column+1][value_index]
                        bottom_left = pixel_matrix[row+1][column-1][value_index]
                        bottom_right = pixel_matrix[row+1][column+1][value_index]
                        # diagonal 4-point average
                        pixel_matrix[row][column][value_index] = arithmetic_mean((
                            top_left, top_right,
                            bottom_left, bottom_right
                        ))

    return pixel_matrix


def four_point_filling_1(pixel_matrix: numpy.ndarray) -> numpy.ndarray:
    """Four point filling v1"""

    # 1) diagonal 4-point: pos_5 =
    #   arithmetic_mean_int((pos_7, pos_9, pos_1, pos_2)) where all 4 are original pixels
    # 2) horizontal 4-point: pos_5 =
    #   arithmetic_mean_int((pos_8, pos_2, pos_4, pos_6)) where pos_4 and pos_6 are original pixels
    # 3) vertical 4-point: pos_5 =
    #   arithmetic_mean_int((pos_8, pos_2, pos_4, pos_6)) where pos_8 and pos_2 are original pixels

    pixel_matrix = double_pixels_1(pixel_matrix)

    return pixel_matrix


def main() -> None:
    """Main"""

    parser = ArgumentParser()

    parser.add_argument('-i', '--input-file', metavar='PATH',
                        required=True, type=type_file_path,
                        dest='input_file')

    parser.add_argument('-o', '--output-file', metavar='PATH',
                        default=None, type=type_file_path,
                        dest='output_file')

    args: Namespace = parser.parse_args()

    print('Input file:', args.input_file)
    source_image: Image = Image.open(args.input_file)

    # attempt to ensure image is RGB
    source_rgb: Image = source_image.convert(mode='RGB')

    pixel_matrix: numpy.ndarray = numpy.asarray(source_rgb)

    print('Source image height:', len(pixel_matrix))
    print('Source image width: ', len(pixel_matrix[1]))

    # not optioned yet, default is present
    pixel_matrix_modified: numpy.ndarray = two_point_filling_1(pixel_matrix)

    final_image: Image = Image.fromarray(pixel_matrix_modified, 'RGB')

    if args.output_file is None:
        input_file_part_name, input_file_part_ext = os.path.splitext(args.input_file)
        output_file = f'{input_file_part_name}-output{input_file_part_ext}'
    else:
        output_file = args.output_file

    print('Output file:', output_file)
    final_image.save(output_file)


if __name__ == '__main__':
    main()
