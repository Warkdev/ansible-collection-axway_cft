#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_transfer
short_description: Perform action on the given transfer.
description:
  - Perform the given action on the transfer corresponding to the provided idtu.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    direction:
        description: Transfer direction
        type: str
        choices:
        - RECV
        - SEND 
    part:
        description: Partner of the transfer
        type: str
    idf:
        description: Flow identifier.
        type: str
    apitimeout:
        description: Command timeout.
        type: int
    fname:
        description: File to be sent.
        type: str
    parm:
        description: Additional information about the transfer.
        type: str
    idm:
        description: Message identifier.
        type: str
    msg:
        description: Message data
        type: str
    idtu:
        description: Transfer ID.
        type: str
    msg:
        description: Message to be provided in the acknowledgement.
        type: str
    state:
        description: State of the transfer after this module is executed
        type: str
        required: true
        default: present
        choices:
        - present
        - absent
        - halted
        - kept
        - started
        - resumed
        - submitted
        - acknowledged
        - nacknowleged
        - ended
'''

EXAMPLES = r'''
- name: Send a new transfer message
  axway_cft_transfer:
    part: PARIS
    idm: MESSAGEID
    msg: My little message

- name: Create a new send file transfer request
  axway_cft_transfer:
    direct: SEND
    part: PARIS
    idf: SMSU001
    fname: C:/tmp/my_file.txt

- name: Create a new receive file transfer request
  axway_cft_transfer:
    direct: RECV
    part: NEWYORK
    idf: SMSU002
    fname: C:/tmp/my_incoming_file.txt

- name: Delete a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: absent

- name: Halt a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: halted

- name: Keep a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: kept

- name: Start a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: started

- name: Resume a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: resumed

- name: Submit a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: submitted

- name: Ack a given transfer
  axway_cft_transfer:
    idtu: T1234567
    idm: M001
    msg: Validate the transfer
    state: acknowledged

- name: Nack a given transfer
  axway_cft_transfer:
    idtu: T1234567
    idm: M001
    msg: Invalidate the transfer
    state: nacknowledged

- name: End a given transfer
  axway_cft_transfer:
    idtu: T1234567
    state: ended
'''

RETURN = r'''
transfer:
    description: The transfer created
    returned: created
    type: dict
    sample:
        partner: string
        idf: string
        idtu: string
        idt: string
        state: string
        phase: string
        phasestep: string
        ida: string
        diagi: string
        diagp: string
        links:
            rel: string
            href: string
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_cft_transfers import fetch_transfer

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
            idtu=dict(type='str'),
            state=dict(type='str', required=True, default='present', choices=['present', 'absent', 'halted', 'kept', 'started', 'resumed', 'submitted', 'acknowledged', 'nacknowledged', 'ended'])
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_if = [
            ['state', 'present', ['direct', 'part', 'idf', 'fname', 'idm', 'msg'], True],
            ['state', 'absent', ['idtu']],
            ['state', 'halted', ['idtu']],
            ['state', 'kept', ['idtu']],
            ['state', 'started', ['idtu']],
            ['state', 'resumed', ['idtu']],
            ['state', 'submitted', ['idtu']],
            ['state', 'acknowledged', ['idtu', 'idm', 'msg']],
            ['state', 'nacknowleged', ['idtu', 'idm', 'msg']],
            ['state', 'ended', ['idtu']]
        ]
        self.mutually_exclusive = [
            ['direct', 'idm'],
            ['direct', 'msg'],
            ['idf', 'idm'],
            ['idf', 'msg'],
            ['fname', 'idm'],
            ['fname', 'msg']
        ]
        self.required_by = {
            'direct': ['part', 'idf', 'fname'],
            'idm': ['msg']
        }


def __exec_post(module, **kwargs):
    pass


def __exec_delete(module, **kwargs):
    pass


def __exec_halt(module, **kwargs):
    pass


def __exec_keep(module, **kwargs):
    pass


def __exec_start(module, **kwargs):
    pass


def __exec_resume(module, **kwargs):
    pass


def __exec_submit(module, **kwargs):
    pass


def __exec_ack(module, **kwargs):
    pass


def __exec_nack(module, **kwargs):
    pass


def __exec_end(module, **kwargs):
    pass


def exec_module(module):
    state = module.params.pop('state')

    if state == 'present':
        response = __exec_post(module=module, **module.params)
    elif state == 'absent':
        response = __exec_delete(module=module, **module.params)
    elif state == 'halted':
        response = __exec_halt(module=module, **module.params)
    elif state == 'kept':
        response = __exec_keep(module=module, **module.params)
    elif state == 'started':
        response = __exec_start(module=module, **module.params)
    elif state == 'resumed':
        response = __exec_resume(module=module, **module.params)
    elif state == 'submitted':
        response = __exec_submit(module=module, **module.params)
    elif state == 'acknowledged':
        response = __exec_ack(module=module, **module.params)
    elif state == 'nacknowledged':
        response = __exec_nack(module=module, **module.params)
    elif state == 'ended':
        response = __exec_end(module=module, **module.params)
    
    return {}


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        required_if=spec.required_if,
        mutually_exclusive=spec.mutually_exclusive,
        required_by=spec.required_by
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
