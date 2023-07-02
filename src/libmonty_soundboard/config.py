#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Config
"""

# imports: library
from dataclasses import dataclass, InitVar, field
import json
import os


@dataclass
class SoundboardItem:
    """Soundboard item"""

    filename: str
    text: str


@dataclass
class Config:
    """Config"""

    main_file_path: InitVar[str]

    _main_dir: str = None
    _data_dir: str = None

    board_name: str = None

    title: str = 'Soundboard'
    sound_items: list[SoundboardItem] = field(default_factory=list)

    def __post_init__(self, main_file_path: str):
        self._main_dir = os.path.split(os.path.abspath(main_file_path))[0]
        self._data_dir = os.path.join(self._main_dir, 'data')

    def data_path(self, *elements) -> str:
        """Data path"""

        return os.path.join(self._data_dir, *elements)

    def data_path_board(self, *elements) -> str:
        """Data path board"""

        return os.path.join(self._data_dir, self.board_name, *elements)

    def load(self, name):
        """Load"""

        self.board_name = name

        path: str = self.data_path(self.board_name, 'config.json')

        with open(path, 'rb') as fh_config:
            config_json = json.load(fh_config)

        self.title = config_json['title']

        self.sound_items = []
        for item in config_json['sounds']:
            self.sound_items.append(SoundboardItem(item['filename'], item['text']))
