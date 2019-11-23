#!/usr/bin/env python3

def boldText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[1m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def faintText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[2m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def italicText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[3m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def underlinedText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[4m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def blinkingText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[5m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def imageNegativeText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[7m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def primaryFontText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[10m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def alternateFontText(argFunction):
    def newFunction(argPrintable, argAlternateFontNo):
        if int(argAlternateFontNo) > 0 and int(argAlternateFontNo) < 10:
            insertedNo = str(argAlternateFontNo)
        else:
            insertedNo = "1"
        return "\x1b[1" + insertedNo + "m" + str(argFunction(argPrintable, argAlternateFontNo)) + "\x1b[0m"
    return newFunction

def blackText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[30m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def redText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[31m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def greenText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[32m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def yellowText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[33m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def blueText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[34m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def magentaText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[35m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def cyanText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[36m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def whiteText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[37m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgBlackText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[40m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgRedText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[41m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgGreenText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[42m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgYellowText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[43m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgBlueText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[44m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgMagentaText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[45m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgCyanText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[46m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def bgWhiteText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[47m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def framedText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[51m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def encircledText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[52m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

def overlinedText(argFunction):
    def newFunction(argPrintable):
        return "\x1b[53m" + str(argFunction(argPrintable)) + "\x1b[0m"
    return newFunction

