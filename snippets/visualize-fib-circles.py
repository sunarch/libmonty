# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# imports ######################################################################

import pygame

# main function ################################################################

def main():

    PRIME_1_DIGIT = 7   # largest 1 digit prime
    PRIME_2_DIGIT = 97  # largest 2 digit prime

    # the first prime of every hundred with an order below 100
    # '503' excluded to keep under 500
    CIRCLE_RADIUS_POSSIBILITIES = [101, 211, 307, 401]
    CIRCLE_RADIUS_POSSIBILITIES_LENGTH = len(CIRCLE_RADIUS_POSSIBILITIES)

    WINDOW_SIZE = 1000
    WINDOW_WIDTH = WINDOW_SIZE
    WINDOW_HEIGHT = WINDOW_SIZE
    WINDOW_CAPTION = "Visualizer"

    BACKGROUND_COLOR = (0, 0, 0)

    TITLE_FONTSIZE = 36
    TITLE_COLOR = (128, 128, 255)
    title_text = "[ press space to begin ]"

    CIRCLE_COLOR = (255, 0, 0)
    CIRCLE_POSITION_X = int(WINDOW_WIDTH / 2)
    CIRCLE_POSITION_Y = int(WINDOW_HEIGHT / 2)
    circle_radius = int(WINDOW_SIZE / 3)
    circle_width = int(circle_radius / 3)

    fib_current_iteration = 0
    fib_prev_number = 0
    fib_current_number = 0
    fib_next_number = 1

    # p_display (screen/window)
    pygame.init()
    p_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_CAPTION)

    # p_surface (background)
    p_surface = pygame.Surface(p_display.get_size())
    p_surface = p_surface.convert()
    p_surface.fill(BACKGROUND_COLOR)

    # Display some text
    font = pygame.font.Font(None, TITLE_FONTSIZE)
    text = font.render(title_text, 1, TITLE_COLOR)
    textpos = text.get_rect()
    textpos.centerx = p_surface.get_rect().centerx
    textpos.centery = p_surface.get_rect().centery
    p_surface.blit(text, textpos)

    # Blit everything to the screen
    p_display.blit(p_surface, (0, 0))
    pygame.display.flip()

    # Event loop ###############################################################
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                p_surface.fill(BACKGROUND_COLOR)

                circle_radius = int(CIRCLE_RADIUS_POSSIBILITIES[fib_current_number % CIRCLE_RADIUS_POSSIBILITIES_LENGTH])

                circle_width = int(fib_current_number % PRIME_2_DIGIT)
                if circle_width < PRIME_1_DIGIT: circle_width = PRIME_1_DIGIT

                title_text = str(fib_current_iteration) + ". | " +  '{0:,}'.format(fib_current_number) + " || R = " + str(circle_radius) + " || W = " + str(circle_width)

                font = pygame.font.Font(None, TITLE_FONTSIZE)
                text = font.render(title_text, 1, TITLE_COLOR)
                textpos = text.get_rect()
                textpos.centerx = p_surface.get_rect().centerx
                textpos.centery = int((TITLE_FONTSIZE / 2) + 20)
                p_surface.blit(text, textpos)

                pygame.draw.circle(p_surface, CIRCLE_COLOR, (CIRCLE_POSITION_X, CIRCLE_POSITION_Y), circle_radius, circle_width)

                fib_current_iteration += 1
                fib_prev_number = fib_current_number
                fib_current_number = fib_next_number
                fib_next_number = fib_prev_number + fib_current_number

        p_display.blit(p_surface, (0, 0))
        pygame.display.flip()

# start program ################################################################

if __name__ == '__main__': main()

# END ##########################################################################
