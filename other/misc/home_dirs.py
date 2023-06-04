#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path


def _user_home():
    return os.path.expanduser('~')


def _environ_or_default(env_name: str, default_path: str, create: bool = False) -> str:
    path = None

    try:
        try:
            env_var = os.environ[env_name]
        except KeyError:
            raise ValueError
        else:
            if not os.path.isdir(env_var):
                raise ValueError
            path = env_var

    except ValueError:
        path_elements = default_path.split('/')
        expanded_path = map(lambda element: element.replace('$HOME', _user_home()),
                            path_elements)
        path = os.path.join(*expanded_path)

    if create:
        if not os.path.isdir(path):
            os.makedirs(path, mode=0o740, exist_ok=True)

    return path


def data(create: bool = False):
    """user-specific data files"""
    return _environ_or_default('XDG_DATA_HOME', '$HOME/.local/share', create=create)


def config(create: bool = False):
    """user-specific configuration files"""
    return _environ_or_default('XDG_CONFIG_HOME', '$HOME/.config', create=create)


def cache(create: bool = False):
    """user-specific non-essential data files"""
    return _environ_or_default('XDG_CACHE_HOME', '$HOME/.cache', create=create)
