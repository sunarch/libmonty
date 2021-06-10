# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from libmonty.network import responses
from libmonty.images import convert_from_stream as img_convert

from libmonty.pixels import config
from libmonty.pixels import output

from libmonty.pixels import api_get_pixel
from libmonty.pixels import api_get_pixels
from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel

MAX_CONSOLE_LOG_LENGTH = 110


def main(args: list[str], kwargs: dict) -> None:

    config.load_token_env()

    output.archive_old_files()

    s_timestamp = output.log_filename()

    with open(output.log_path(s_timestamp), "wt", encoding="utf-8") as f_log:
        output.output(output.form_separator(), f_log)
        output.output(f"Pixels log: {s_timestamp}", f_log)
        output.output(output.form_separator(), f_log)

    d_struct = None

    # api_get_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "get" and args[1] == "head":
        result = api_get_pixel.headers()
        log_result(s_timestamp, result)

    if len(args) == 3 and args[0] == "get":
        result = api_get_pixel.execute(int(args[1]), int(args[2]))
        log_result(s_timestamp, result)

    # api_get_pixels ---------------------------------------------------

    image_commands = ("img", "image")

    if len(args) == 2 and args[0] in image_commands and args[1] == "head":
        result = api_get_pixels.headers()
        log_result(s_timestamp, result)

    if len(args) == 1 and args[0] in image_commands:

        result_s = api_get_size.execute()
        log_result(s_timestamp, result_s)

        result_p = api_get_pixels.execute()
        log_result(s_timestamp, result_p)

        try:
            img_convert.rgb(output.FOLDER_IMG,
                            s_timestamp,
                            result_p['bytes'],
                            (result_s['width'],  result_s['height']),
                            scale=8)
        except KeyError:
            pass

    # api_get_size -----------------------------------------------------

    if len(args) == 1 and args[0] == "size":
        result = api_get_size.execute()
        log_result(s_timestamp, result)

    # api_set_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "set" and args[1] == "head":
        result = api_set_pixel.headers()
        log_result(s_timestamp, result)

    if len(args) == 4 and args[0] == "set":
        result = api_set_pixel.execute(int(args[1]), int(args[2]), args[3])
        log_result(s_timestamp, result)


def log_result(timestamp: str, result: dict) -> None:

    with open(output.log_path(timestamp), "at", encoding="utf-8") as f_log:

        s_request = f'"{result["request_name"]}"'
        try:
            for s_key in result['request_arguments']:
                s_request += f" <{s_key}: {result['request_arguments'][s_key]}>"
        except KeyError:
            pass
        output.output(f"API request: {s_request}", f_log)

    if result is not None:

        response = result['response']

        with open(output.log_path(timestamp), "at", encoding="utf-8") as f_log:

            i_status = response.status_code
            s_status_title = responses.get(i_status)['title']
            s_status = f"{i_status} - {s_status_title}"

            output.output(f"Response:    {s_status}", f_log)

            s_type = result['data_type']
            s_enc = result['data_encoding']
            s_data = result['data']

            output.output(f'Data:        ({s_type}/{s_enc}) "{s_data}"', f_log)

            if len(config.parse_headers(response.headers)) > 0:
                output.section_response_headers(response.headers, f_log)

            output.output(output.form_separator(), f_log)

# -------------------------------------------------------------------- #
