#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_flows_info
short_description: Retrieves detailed content about flow objects.
description:
  - Retrieve flow objects specified by the given type
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    type:
        description: Type of flow object to return
        type: str
        required: true
        choices:
        - CFTSEND
        - CFTRECV
        - CFTPART
        - CFTDEST
    offset:
        description: Number of objects to skip
        type: int
        default: 0
    limit:
        description: Number of objects to return
        type: int
        default: 100
'''

EXAMPLES = r'''
- name: Gather flows info for CFTSEND
  axway_cft_flows_info:
    type: CFTSEND
  register: flows_cftsend

- name: Gather flows info for CFTRECV
  axway_cft_flows_info:
    type: CFTRECV
  register: flows_cftrecv

- name: Gather flows info for CFTPART
  axway_cft_flows_info:
    type: CFTPART
  register: flows_cftpart

- name: Gather flows info for CFTDEST
  axway_cft_flows_info:
    type: CFTDEST
  register: flows_cftdest
'''

RETURN = r'''
cftsend:
    description: The CFTSEND objects configured
    returned: success
    type: list
    elements: dict
    sample:
        id: string

cftrecv:
    description: The CFTRECV objects configured
    returned: success
    type: list
    elements: dict
    sample:
        id: string

cftpart:
    description: The CFTPART objects configured
    returned: success
    type: list
    elements: dict
    sample:
        id: string

cftdest:
    description: The CFTDEST objects configured
    returned: success
    type: list
    elements: dict
    sample:
        id: string
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_cft_objects import fetch_cftdest, fetch_cftpart, fetch_cftrecv, fetch_cftsend

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            type=dict(type='str', required=True, choices=['CFTSEND', 'CFTRECV', 'CFTPART', 'CFTDEST']),
            offset=dict(type='int', default=0),
            limit=dict(type='int', default=100)
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_get(module, **kwargs):
    if kwargs['type'] == 'CFTSEND':
        response = fetch_cftsend(module=module, offset=kwargs['offset'], limit=kwargs['limit'])
    elif kwargs['type'] == 'CFTRECV':
        response = fetch_cftrecv(module=module, offset=kwargs['offset'], limit=kwargs['limit'])
    elif kwargs['type'] == 'CFTPART':
        response = fetch_cftpart(module=module, offset=kwargs['offset'], limit=kwargs['limit'])
    elif kwargs['type'] == 'CFTDEST':
        response = fetch_cftdest(module=module, offset=kwargs['offset'], limit=kwargs['limit'])
    return response


def exec_module(module):
    response = __exec_get(module=module, **module.params)
    return response


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    try:
        setup_logging(str_log, module._verbosity)
        logger.debug('Module parameters %s', module.params)

        response = exec_module(module)
        return_value = create_return_object()
        update_logging_info(return_value, str_log.getvalue(), error_log.getvalue())
        return_value.update(response)

        module.exit_json(**return_value)
    except Exception as e:
        error_log.write(get_traceback(e))
        return_value = create_return_error(msg=str(e), stdout=str_log.getvalue(), stderr=error_log.getvalue())
        module.fail_json(**return_value)


if __name__ == '__main__':
    main()
