# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.parsing.convert_bool import (
    BOOLEANS_TRUE, BOOLEANS_FALSE
)

import re


def flattened_to_bool(value):
    return flatten_boolean(value) == 'yes'


def flatten_boolean(value):
    truthy = list(BOOLEANS_TRUE) + ['enabled', 'True', 'true', 'YES']
    falsey = list(BOOLEANS_FALSE) + ['disabled', 'False', 'false', 'NO']
    if value is None:
        return None
    elif value in truthy:
        return 'yes'
    elif value in falsey:
        return 'no'


def build_query_str(**kwargs):
    query_str = ''
    for param in kwargs:
        if kwargs[param]:
            query_str = '{0}&{1}={2}'.format(query_str, param, kwargs[param])

    return query_str[1:]  # Remove leading '&' character


def build_payload(**kwargs):
    payload = {}
    for param in kwargs:
        if kwargs[param]:
            payload.update({param: kwargs[param]})

    return payload


def validate_arg_pattern(name, value, pattern):
    try:
        re.compile(pattern)
        re.fullmatch(value)
    except Exception:
        raise AxwayModuleError("The argument {0} doesn't match the expected pattern {1}".format(name, pattern))


class Noop(object):
    pass


class AxwayModuleError(Exception):
    pass
