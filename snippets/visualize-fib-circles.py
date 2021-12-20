#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports ######################################################################

import pygame


# main function ################################################################

def main():

    prime_1_digit = 7   # largest 1 digit prime
    prime_2_digit = 97  # largest 2 digit prime

    # the first prime of every hundred with an order below 100
    # '503' excluded to keep under 500
    circle_radius_possibilities = [101, 211, 307, 401]
    circle_radius_possibilities_length = len(circle_radius_possibilities)

    window_size = 1000
    window_width = window_size
    window_height = window_size
    window_caption = "Visualizer"

    background_color = (0, 0, 0)

    title_fontsize = 36
    title_color = (128, 128, 255)
    title_text = "[ press space to begin ]"

    circle_color = (255, 0, 0)
    circle_position_x = int(window_width / 2)
    circle_position_y = int(window_height / 2)
    circle_radius = int(window_size / 3)
    circle_width = int(circle_radius / 3)

    fib_current_iteration = 0
    fib_prev_number = 0
    fib_current_number = 0
    fib_next_number = 1

    # p_display (screen/window)
    pygame.init()
    p_display = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_caption)

    # p_surface (background)
    p_surface = pygame.Surface(p_display.get_size())
    p_surface = p_surface.convert()
    p_surface.fill(background_color)

    # Display some text
    font = pygame.font.Font(None, title_fontsize)
    text = font.render(title_text, True, title_color)
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
                p_surface.fill(background_color)

                circle_radius = int(circle_radius_possibilities[fib_current_number % circle_radius_possibilities_length])

                circle_width = int(fib_current_number % prime_2_digit)
                if circle_width < prime_1_digit:
                    circle_width = prime_1_digit

                title_text = f'{fib_current_iteration}. | {fib_current_number}'
                title_text += f' || R = {circle_radius} || W = {circle_width}'

                font = pygame.font.Font(None, title_fontsize)
                text = font.render(title_text, True, title_color)
                textpos = text.get_rect()
                textpos.centerx = p_surface.get_rect().centerx
                textpos.centery = int((title_fontsize / 2) + 20)
                p_surface.blit(text, textpos)

                pygame.draw.circle(p_surface, circle_color, (circle_position_x, circle_position_y), circle_radius, circle_width)

                fib_current_iteration += 1
                fib_prev_number = fib_current_number
                fib_current_number = fib_next_number
                fib_next_number = fib_prev_number + fib_current_number

        p_display.blit(p_surface, (0, 0))
        pygame.display.flip()


# start program ################################################################

if __name__ == '__main__':
    main()

# END ##########################################################################
