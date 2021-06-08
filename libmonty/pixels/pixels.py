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

    config.load_token_once()

    output.archive_old_files()

    s_timestamp = output.log_filename()

    with open(output.log_path(s_timestamp), "wt", encoding="utf-8") as f_log:
        output.output(output.construct_heading("Pixels log:"), f_log)
        output.output(f"Timestamp:   '{s_timestamp}'", f_log)

    d_struct = None

    # api_get_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "get" and args[1] == "head":
        s_api_request_name, result = api_get_pixel.headers()
        log_result(s_timestamp, s_api_request_name, result)

    if len(args) == 3 and args[0] == "get":
        s_api_request_name, result = api_get_pixel.execute(int(args[1]), int(args[2]))
        log_result(s_timestamp, s_api_request_name, result)

    # api_get_pixels ---------------------------------------------------

    image_commands = ("img", "image")

    if len(args) == 2 and args[0] in image_commands and args[1] == "head":
        s_api_request_name, result = api_get_pixels.headers()
        log_result(s_timestamp, s_api_request_name, result)

    if len(args) == 1 and args[0] in image_commands:

        s_api_request_name_s, result_s = api_get_size.execute()
        log_result(s_timestamp, s_api_request_name_s, result_s)

        s_api_request_name_p, result_p = api_get_pixels.execute()
        log_result(s_timestamp, s_api_request_name_p, result_p)

        try:
            img_convert.rgb(output.FOLDER_IMG,
                            s_timestamp,
                            result_p['data'],
                            (result_s['width'],  result_s['height']),
                            scale=8)
        except KeyError:
            pass

    # api_get_size -----------------------------------------------------

    if len(args) == 1 and args[0] == "size":
        s_api_request_name, result = api_get_size.execute()
        log_result(s_timestamp, s_api_request_name, result)

    # api_set_pixel ----------------------------------------------------

    if len(args) == 2 and args[0] == "set" and args[1] == "head":
        s_api_request_name, result = api_set_pixel.headers()
        log_result(s_timestamp, s_api_request_name, result)

    if len(args) == 4 and args[0] == "set":
        s_api_request_name, result = api_set_pixel.execute(int(args[1]), int(args[2]), args[3])
        log_result(s_timestamp, s_api_request_name, result)


def log_result(timestamp: str, api_request_name: str, result: dict) -> None:

    with open(output.log_path(timestamp), "at", encoding="utf-8") as f_log:

        output.output(f"API request: '{api_request_name}'", f_log)

        output.output(output.construct_heading("Data:"), f_log)

        i_longest_tag = 1
        for s_field in result:
            if s_field != "response":
                if len(s_field) > i_longest_tag:
                    i_longest_tag = len(s_field)

        for s_field in result:
            if s_field != "response":

                s_tag = f"'{s_field}'"
                s_title = f"{s_tag:<{i_longest_tag + 2}}"

                try:
                    s_content = f"'{result[s_field]}'"

                    try:
                        if len(result[s_field]) < MAX_CONSOLE_LOG_LENGTH:
                            output.output(f"{s_title} : {s_content}", f_log)
                        else:
                            output.to_log(f"{s_title} : {s_content}", f_log)
                            output.to_console(f"{s_title} : <data | length: {len(result[s_field])}>")
                    except TypeError:
                        output.output(f"{s_title} : {s_content}", f_log)

                except AttributeError:
                    output.output(f"{s_title} : AttributeError", f_log)

    if result is not None:

        response = result['response']

        with open(output.log_path(timestamp), "at", encoding="utf-8") as f_log:

            output.output(output.construct_heading("Response:"), f_log)

            i_status = response.status_code
            s_status_title = responses.get(i_status)['title']

            output.output(f"Status code: '{i_status}' - {s_status_title}", f_log)
            output.output(f"Encoding:    '{response.encoding}'", f_log)

            if len(response.text) < MAX_CONSOLE_LOG_LENGTH:
                output.output(f"Text:        '{response.text}'", f_log)
            else:
                output.to_log(f"Text:        '{response.text}'", f_log)
                output.to_console(f"Text:        <data | length: {len(response.text)}>")

            try:
                s_json = f"'{response.json()}'"
            except json.JSONDecodeError:
                s_json = "Invalid JSON data."

            output.output(f"JSON:        {s_json}", f_log)

            if len(config.parse_headers(response.headers)) > 0:
                output.section_response_headers(response.headers, f_log)

            output.output(output.construct_heading(""), f_log)

# -------------------------------------------------------------------- #
