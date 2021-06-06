# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib.formatting.terminaltextstyles import *


def displayErrorMessage(error):
    print(strBold(strRed("Error")) + ", " + error.args[0])

def errorMessage(message):
    print(strBold(strRed("Error")) + ", " + message )

def warningMessage(message):
    print(strBold(strYellow("Warning")) + ", " + message )

def infoMessage(message):
    print(strBold(strBlue("Info")) + ", " + message )
