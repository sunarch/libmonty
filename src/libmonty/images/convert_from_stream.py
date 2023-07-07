#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Convert image from stream
"""

# imports: requirements
import PIL.Image

# modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

# MODE "RGB" : (3x8-bit pixels, true color)

_DECODER_RAW: str = 'raw'


def rgb(folder: str,
        filename: str,
        data: bytes,
        size: tuple[int, int],
        scale: int = None) -> None:
    """RGB"""

    width, height = size

    img = PIL.Image.frombytes('RGB', size, data, decoder_name=_DECODER_RAW)
    img.save(f'{folder}/{filename}.png')

    if scale is not None:

        scaled_size = (width * 8, height * 8)

        img2 = PIL.Image.frombytes('RGB', size, data, decoder_name=_DECODER_RAW)
        img2 = img2.resize(scaled_size, resample=PIL.Image.NEAREST)
        img2.save(f'{folder}/{filename}-scale-{scale}.png')
