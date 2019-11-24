# Output decorators with ASCII escape sequences
# Version 1.1

# https://en.wikipedia.org/wiki/ANSI_escape_code

# Python utilites
# https://github.com/sunarch/libmonty
# 'utils' folder


def boldText(arg_function):
    def new_function(arg_printable):
        return "\x1b[1m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def faintText(arg_function):
    def new_function(arg_printable):
        return "\x1b[2m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def italicText(arg_function):
    def new_function(arg_printable):
        return "\x1b[3m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def underlinedText(arg_function):
    def new_function(arg_printable):
        return "\x1b[4m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def blinkingText(arg_function):
    def new_function(arg_printable):
        return "\x1b[5m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def imageNegativeText(arg_function):
    def newFunction(arg_printable):
        return "\x1b[7m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def primaryFontText(argFunction):
    def newFunction(arg_printable):
        return "\x1b[10m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def alternateFontText(arg_function):
    def new_function(arg_printable, arg_alternate_font_no):
        inserted_no = "1"
        if int(arg_alternate_font_no) in range(1, 10): # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)
        return "\x1b[1{0}m{1}\x1b[0m".format(inserted_no, arg_function(arg_printable, arg_alternate_font_no))
    return new_function

def blackText(arg_function):
    def new_function(arg_printable):
        return "\x1b[30m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def redText(arg_function):
    def new_function(arg_printable):
        return "\x1b[31m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def greenText(arg_function):
    def new_function(arg_printable):
        return "\x1b[32m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def yellowText(arg_function):
    def new_function(arg_printable):
        return "\x1b[33m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def blueText(arg_function):
    def new_function(arg_printable):
        return "\x1b[34m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def magentaText(arg_function):
    def new_function(arg_printable):
        return "\x1b[35m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def cyanText(arg_function):
    def new_function(arg_printable):
        return "\x1b[36m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def whiteText(arg_function):
    def new_function(arg_printable):
        return "\x1b[37m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgBlackText(arg_function):
    def new_function(arg_printable):
        return "\x1b[40m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgRedText(arg_function):
    def new_function(arg_printable):
        return "\x1b[41m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgGreenText(arg_function):
    def new_function(arg_printable):
        return "\x1b[42m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgYellowText(arg_function):
    def new_function(arg_printable):
        return "\x1b[43m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgBlueText(arg_function):
    def new_function(arg_printable):
        return "\x1b[44m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgMagentaText(arg_function):
    def new_function(arg_printable):
        return "\x1b[45m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgCyanText(arg_function):
    def new_function(arg_printable):
        return "\x1b[46m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def bgWhiteText(arg_function):
    def new_function(arg_printable):
        return "\x1b[47m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def framedText(arg_function):
    def new_function(arg_printable):
        return "\x1b[51m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def encircledText(arg_function):
    def new_function(arg_printable):
        return "\x1b[52m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

def overlinedText(arg_function):
    def new_function(arg_printable):
        return "\x1b[53m{0}\x1b[0m".format(arg_function(arg_printable))
    return new_function

