# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import time


FOLDER_LOGS = "libmonty/pixels/logs"
FOLDER_LOGS_ARCHIVE = "libmonty/pixels/logs/archive"

FOLDER_IMG = "libmonty/pixels/canvas"
FOLDER_IMG_ARCHIVE = "libmonty/pixels/canvas/archive"


def log_path(timecode: str) -> str:

    return f"{FOLDER_LOGS}/{timecode}.txt"


def log_filename() -> str:

    return time.strftime("%Y-%m-%d-t-%H-%M-%S-z", time.gmtime())


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

# -------------------------------------------------------------------- #
