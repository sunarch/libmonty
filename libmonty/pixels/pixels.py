# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.images import convert_from_stream as img_convert

from libmonty.pixels import config
from libmonty.pixels import output
from libmonty.pixels import files

from libmonty.pixels import api_get_pixel
from libmonty.pixels import api_get_pixels
from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel


def main(args: list[str], kwargs: dict) -> None:

    config.load_token_env()

    files.archive_old_files()

    s_timestamp = files.log_filename()

    with open(files.log_path(s_timestamp), "wt", encoding="utf-8") as f_log:
        output.to_all(output.form_separator(), f_log)
        output.to_all(f"Pixels log: {s_timestamp}", f_log)
        output.to_all(output.form_separator(), f_log)

    # api_get_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "get" and args[1] == "head":
        result = api_get_pixel.headers()
        output.log_result(s_timestamp, result)

    if len(args) == 3 and args[0] == "get":
        result = api_get_pixel.execute(int(args[1]), int(args[2]))
        output.log_result(s_timestamp, result)

    # api_get_pixels ---------------------------------------------------

    image_commands = ("img", "image")

    if len(args) == 2 and args[0] in image_commands and args[1] == "head":
        result = api_get_pixels.headers()
        output.log_result(s_timestamp, result)

    if len(args) == 1 and args[0] in image_commands:
        cmd_image(s_timestamp)

    # api_get_size -----------------------------------------------------

    if len(args) == 1 and args[0] == "size":
        result = api_get_size.execute()
        output.log_result(s_timestamp, result)

    # api_set_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "set" and args[1] == "head":
        result = api_set_pixel.headers()
        output.log_result(s_timestamp, result)

    if len(args) == 4 and args[0] == "set":
        result = api_set_pixel.execute(int(args[1]), int(args[2]), args[3])
        output.log_result(s_timestamp, result)


def cmd_image(timestamp: str):

    result_s = api_get_size.execute()
    output.log_result(timestamp, result_s)

    result_p = api_get_pixels.execute()
    output.log_result(timestamp, result_p)

    try:
        img_convert.rgb(files.FOLDER_IMG,
                        timestamp,
                        result_p['bytes'],
                        (result_s['width'], result_s['height']),
                        scale=8)
    except KeyError:
        pass

# -------------------------------------------------------------------- #
