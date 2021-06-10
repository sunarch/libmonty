# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.network import responses

from libmonty.pixels import files
from libmonty.pixels import api_headers


def to_console(content: str) -> None:
    print(content, end="\n")


def to_log(content: str, f_log) -> None:
    f_log.write(f"{content}" + "\n")


def to_all(content: str, f_log) -> None:
    to_log(content, f_log)
    to_console(content)


def form_separator() -> str:

    return "-" * 72


def form_request_input(name: str, arguments: dict) -> str:

    s_request = f'"{name}"'

    for s_key in arguments:
        s_request += f" <{s_key}: {arguments[s_key]}>"

    return f"API request: {s_request}"


def log_result(timestamp: str, result: dict) -> None:

    with open(files.log_path(timestamp), "at", encoding="utf-8") as f_log:

        if result is None:
            to_log(f"Result is None.", f_log)
            return

        try:
            d_arguments = result['request_arguments']
        except KeyError:
            d_arguments = {}

        s_request = form_request_input(result["request_name"], d_arguments)
        to_log(s_request, f_log)

        response = result['response']

        i_status = response.status_code
        s_status_title = responses.get(i_status)['title']
        s_status = f"{i_status} - {s_status_title}"

        to_log(f"Response:    {s_status}", f_log)

        if result['data']:

            s_type = result['data_type']
            s_enc = result['data_encoding']
            s_data = result['data']

            to_log(f'Data:        ({s_type}/{s_enc}) "{s_data}"', f_log)

        if result['rate_limits']:

            s_remaining = result['rate_limits'][api_headers.RATE_LIMIT_COUNT_REMAINING]
            s_limit = result['rate_limits'][api_headers.RATE_LIMIT_COUNT_LIMIT]
            s_count = f"{s_remaining} / {s_limit}"

            s_reset = result['rate_limits'][api_headers.RATE_LIMIT_TIME_RESET]
            s_period = result['rate_limits'][api_headers.RATE_LIMIT_TIME_PERIOD]
            s_time = f"{s_reset:>3} / {s_period:>3} s"

            to_log(f"Rate limits: {s_count} ({s_time})", f_log)

        if result['cooldown']:

            to_log(f"Cooldown:    {result['cooldown']}", f_log)

        to_log(form_separator(), f_log)

        try:
            regular_response_headers_to_log(result['headers'], f_log)
        except KeyError:
            raise


def regular_response_headers_to_log(headers: dict, f_log) -> None:

    i_longest_tag = 1
    for s_header in headers:
        if len(s_header) > i_longest_tag:
            i_longest_tag = len(s_header)

    for s_header in headers:
        s_tag = f"'{s_header}'"
        s_title = f"{s_tag:<{i_longest_tag + 2}}"
        s_content = f"'{headers[s_header]}'"
        to_log(f"{s_title} : {s_content}", f_log)

    to_log(form_separator(), f_log)

# -------------------------------------------------------------------- #
