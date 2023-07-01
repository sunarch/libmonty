#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
import logging

# imports: requirements
import pygame


class MixerInitError(Exception):
    pass


if not pygame.mixer:
    logging.warning('sound disabled')


def _load_mixer():

    if not pygame.mixer.get_init():
        pygame.mixer.init()

        if (mixer_init := pygame.mixer.get_init()) is not None:
            logging.info('Mixer initalized.')
            mixer_frequency, mixer_format, mixer_channels = mixer_init
            logging.info('frequency: %s', mixer_frequency)
            logging.info('format:    %s', mixer_format)
            logging.info('channels:  %s', mixer_channels)
        else:
            raise MixerInitError('Mixer NOT initalized!')


def load_sound(path):

    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    try:
        _load_mixer()
    except MixerInitError as exc:
        logging.warning(exc)
        return NoneSound()

    sound = pygame.mixer.Sound(path)

    return sound


def deinit() -> None:
    pygame.mixer.quit()
