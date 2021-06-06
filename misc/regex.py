# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re


def RegExMatch(argString, argCompiledPattern):
    match = argCompiledPattern.fullmatch(argString)
    if match:
        return match.groupdict()
    else:
        return None

###############################################################################
######################### REGULAR EXPRESSION MATCHERS #########################
###############################################################################


# examples

REGEX_RULE_CLA = re.compile("^rule=(?P<value>((45|90|270|315)-){4}(45|90|270|315))")
REGEX_SPEEDUP_CLA = re.compile("^speedup=(?P<value>[1-9][0-9]*)")

REGEX_COLOR_ANY = re.compile("(?P<color>[0-4])")
REGEX_OBSTACLE = re.compile("(?P<symbol>\\*)")
REGEX_COORDINATES = re.compile("(?P<row>0|[1-9][0-9]*),(?P<column>0|[1-9][0-9]*)")
REGEX_COUNT = re.compile("(?P<count>([0-9]|[1-9][0-9]*))")

REGEX_ANT_ANY = re.compile("(?P<name>[a-zA-Z])")
REGEX_ANT_DATA = re.compile("(?P<name>[a-zA-Z]),(?P<row>(0|[1-9][0-9]*)),(?P<column>(0|[1-9][0-9]*))")

# matching example

#parsed = RegExMatch(arguments[n], REGEX_RULE_CLA)
#if parsed is not None:
#    newRule = parsed["value"].split("-")
#    for i in range(0, len(rule)):
#        rule[i] = int(newRule[i])
#    continue
