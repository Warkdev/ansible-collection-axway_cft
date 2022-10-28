# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.axway_cft.plugins.module_utils.axway_utils import parse_fail_message
from ansible_collections.community.axway_cft.plugins.module_utils.common import AxwayModuleError, build_query_str
from ansible.module_utils.connection import Connection

import logging

uri = '/logs'

logger = logging.getLogger(__name__)


def fetch_cftdest(module, severity=None, limit=None, datetimemin=None, datetimemax=None, pattern=None):
    """ Retrieves the logs corresponding to the criterias

    Returns:
        _type_: _description_
    """
    query_str = build_query_str(severity=severity, limit=limit, datetimemin=datetimemin, datetimemax=datetimemax, pattern=pattern)
    path = '{0}?{1}'.format(uri, query_str)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path)

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
