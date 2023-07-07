#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Debugging
"""

# imports: project
from libmonty.outpututils.asciistyling import AsciiColor, AsciiStyle


def display_error_message(error: Exception) -> None:
    """Display error message"""

    print(AsciiStyle.bold((AsciiColor.red('Error')) + ', ' + error.args[0]))


def error_message(message: str) -> None:
    """Error message"""

    print(AsciiStyle.bold(AsciiColor.red('Error')) + ', ' + message)


def warning_message(message: str) -> None:
    """Warning message"""

    print(AsciiStyle.bold(AsciiColor.yellow('Warning')) + ', ' + message)


def info_message(message: str) -> None:
    """Info message"""

    print(AsciiStyle.bold(AsciiColor.blue('Info')) + ', ' + message)
