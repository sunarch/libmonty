# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import shutil
import os

from libmonty.pixels import config


FOLDER_LOGS = "libmonty/pixels/logs"
FOLDER_LOGS_ARCHIVE = "libmonty/pixels/logs/archive"

FOLDER_IMG = "libmonty/pixels/canvas"
FOLDER_IMG_ARCHIVE = "libmonty/pixels/canvas/archive"


def log_path(timecode: str) -> str:

    return f"{FOLDER_LOGS}/{timecode}.txt"


def log_filename() -> str:

    return time.strftime("%Y-%m-%d-t-%H-%M-%S-z", time.gmtime())


def to_console(content: str) -> None:
    print(content, end="\n")


def to_log(content: str, f_log) -> None:
    f_log.write(f"{content}" + "\n")


def output(content: str, f_log) -> None:
    to_log(content, f_log)
    to_console(content)


def construct_heading(content: str) -> str:

    return ("-" * 72) + "\n" + content + "\n"


def archive_old_files():

    ls_groups = [
        (FOLDER_LOGS, FOLDER_LOGS_ARCHIVE, ".txt"),
        (FOLDER_IMG, FOLDER_IMG_ARCHIVE, ".png")
    ]

    for t_group in ls_groups:

        ls_files = os.listdir(t_group[0])

        for s_file in ls_files:
            s_path_old = f"{t_group[0]}/{s_file}"
            s_path_new = f"{t_group[1]}/{s_file}"

            if os.path.isfile(s_path_old):
                if t_group[2] in s_file:
                    shutil.move(s_path_old, s_path_new)


def section_response_headers(headers, f_log):

    d_rate_limit_headers = config.parse_headers(headers)

    s_heading = construct_heading("Response headers:")
    to_log(s_heading, f_log)
    if len(d_rate_limit_headers) > 0:
        to_console(s_heading)

    i_longest_tag = 1
    for s_header in headers:
        if len(s_header) > i_longest_tag:
            i_longest_tag = len(s_header)

    for s_header in headers:
        s_tag = f"'{s_header}'"
        s_title = f"{s_tag:<{i_longest_tag + 2}}"
        s_content = f"'{headers[s_header]}'"
        to_log(f"{s_title} : {s_content}", f_log)

        if s_header in config.RATE_LIMIT_HEADER_LABELS:
            to_console(f"{s_title} : {s_content}")

# -------------------------------------------------------------------- #
