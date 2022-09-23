#!/usr/bin/env python3

CODES_C0_CONTROLS = {i for i in range(0, 32)}
CODES_C1_CONTROLS = {i for i in range(128, 161)}
CODES_SKIP_OTHER = {0x2067, 0x206F}
CODES_TO_SKIP = CODES_C0_CONTROLS.union(CODES_C1_CONTROLS, CODES_SKIP_OTHER)

CODES_PLUS_1_WIDTH_CHAR = set().union(

{i for i in range(0x0, 0x0)},

    {0x1B35, 0x202F, 0x231A, 0x231B},
    {0x2329, 0x232A, 0x23E9, 0x23EA, 0x23EB, 0x23EC},
    {0x23F0, 0x23F3, 0x25FE, 0x25FD, 0x2614, 0x2615},
    {i for i in range(0x2648, 0x2653 + 1)},
    {0x267F, 0x2693, 0x26A1, 0x26AA, 0x26AB, 0x26BD, 0x26BE, 0x26C4,
     0x26C5, 0x26CE, 0x26D4, 0x26EA, 0x26F2, 0x26F3, 0x26F5, 0x26FA,
     0x26FD, 0x2705, 0x270A, 0x270B, 0x2728, 0x274C, 0x274E, 0x2753,
     0x2754, 0x2755, 0x2757, 0x2795, 0x2796, 0x2797, 0x27B0, 0x27BF,
     0x2B1B, 0x2B1C, 0x2B50, 0x2B55},
    {i for i in range(0x2E80, 0x2E99)},
    {i for i in range(0x2E9B, 0x2EF3)},
    {i for i in range(0x2F00, 0x2FD5)},
    {i for i in range(0x2FF0, 0x2FFB)},
    {i for i in range(0x3000, 0x3029)},
    {i for i in range(0x302E, 0x303E)},
    {i for i in range(0x3041, 0x3096)},
    {i for i in range(0x3041, 0x3096)},
    {i for i in range(0x3099, 0x30FF)},
    {i for i in range(0x3105, 0x31E3)},
    {i for i in range(0x31F0, 0x321E)},
    {i for i in range(0x3220, 0x3247)},
    {i for i in range(0x3250, 0x4DBF)},
    {i for i in range(0x4E00, 0x7FFF)}
)

CODES_PLUS_2_WIDTH_CHAR = {
    0x2E99, 0x2EF3, 0x2FD5, 0x2FFB, 0x303E, 0x30FF, 0x31E3, 0x321E,
    0x3247, 0x4DBF, 0x7FFF
}

CODES_MINUS_1_WIDTH_CHAR = set().union(

    {0x180B, 0x180C, 0x180D, 0x180E,
        0x1885, 0x1886,
     0x18A9, 0x1920, 0x1921, 0x1922, 0x1927, 0x1928, 0x1932, 0x1939, 0x193A,
     0x193B, 0x1A17, 0x1A18, 0x1A1B, 0x1A56},
    {i for i in range(0x1A58, 0x1A5E + 1)},
    {0x1A60, 0x1A62, 0x1A65},
    {i for i in range(0x1A65, 0x1A6C + 1)},
    {i for i in range(0x1A73, 0x1A7C + 1)},
    {0x1A7F},
    {i for i in range(0x1AB0, 0x1AC0 + 1)},
    {i for i in range(0x1B00, 0x1B03 + 1)},
    {0x1B3A, 0x1B3C},
    {i for i in range(0x1B34, 0x1B39 + 1)},
    {0x1B42},
    {i for i in range(0x1B6B, 0x1B73 + 1)},
    {0x1B80, 0x1B81},
    {i for i in range(0x1BA2, 0x1BA5 + 1)},
    {0x1BA8, 0x1BA9, 0x1BAB, 0x1BAC, 0x1BAD, 0x1BE6, 0x1BE8, 0x1BE9,
     0x1BE9, 0x1BED},
    {i for i in range(0x1BEF, 0x1BF1 + 1)},
    {0x1CD0, 0x1CD1},
    {i for i in range(0x1CD3, 0x1CE0 + 1)},
    {i for i in range(0x1CE2, 0x1CE8 + 1)},
    {0x1CED, 0x1CF4, 0x1CF8, 0x1CF9},
    {i for i in range(0x1DC0, 0x1DF9 + 1)},
    {i for i in range(0x1DFB, 0x1DFF + 1)},
    {i for i in range(0x2060, 0x2064 + 1)},
    {i for i in range(0x2066, 0x206F + 1)},
    {i for i in range(0x202A, 0x202F + 1)},
    {i for i in range(0x20D0, 0x20F0 + 1)},
    {i for i in range(0x2CEF, 0x2CF1)},
    {0x2D7F},
    {i for i in range(0x2DE0, 0x2DFF)},
    {i for i in range(0x302A, 0x302D)}
)

CODES_MINUS_2_WIDTH_CHAR = {0x2CF1, 0x2DFF}


def format_line_start(line_start: str):
    return f'|{line_start}:|'


def print_page(page: int, page_size: int) -> None:

    col_width = 5

    # page header
    header_page_num = f' [ {page:>4} | {hex(page):>5} | {oct(page):>6} ] '
    formatter = '{text:=^' + str(6 + page_size * (col_width + 1)) + '}'
    print(formatter.format(text=header_page_num))
    print('')

    first_code = (page - 1) * page_size
    last_code = first_code + (page_size - 1)

    numerical_headers = [
        ('DEC', ''),
        ('HEX', 'X'),
        ('OCT', 'o')
    ]

    # numerical lines
    for line_start, format_letter in numerical_headers:

        print(format_line_start(line_start), end='')
        for code in range(first_code, last_code + 1):
            formatter = '{code:>' + str(col_width) + format_letter + '}|'
            print(formatter.format(code=code), end='')
        print('')

    # character line
    print(format_line_start('CHR'), end='')
    for code in range(first_code, last_code + 1):
        col_width_char = col_width

        if code in CODES_MINUS_1_WIDTH_CHAR:
            col_width_char += 1
        if code in CODES_MINUS_2_WIDTH_CHAR:
            col_width_char += 1

        if code in CODES_PLUS_1_WIDTH_CHAR:
            col_width_char -= 1
        if code in CODES_PLUS_2_WIDTH_CHAR:
            col_width_char -= 1

        if code in CODES_TO_SKIP:
            print('>' * col_width + '|', end='')
        else:
            try:
                formatter = ' {char:<' + str(col_width_char - 1) + '}|'
                print(formatter.format(char=chr(code)), end='')
            except ValueError:
                print('!' * col_width_char + '|', end='')
    print('')

    # new line after page
    print('')


def main(first_page: int = 1,
         last_page: int = 10,
         page_size: int = 16,
         first_character: int = None,
         last_character: int = None
         ) -> None:

    last_character = 0x17EF  # TODO: remove

    if last_character is not None:
        first_page = first_character // page_size

    if last_character is not None:
        last_page = last_character // page_size + 1

    for page in range(first_page, last_page + 1):
        print_page(page, page_size)


if __name__ == '__main__':
    # last printable character at time of writing
    main(last_character=0x7FFF)
