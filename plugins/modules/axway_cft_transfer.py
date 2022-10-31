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
  - Note that, although check_mode is supported, this module will always return "changed" as result,
    this is due to lack of knowledge from how the product is working.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    ida:
        description: Local transfer identifier. Can be used to create a message or a file transfer. If not provided, the server generates it.
        type: str
    direction:
        description: Transfer direction
        type: str
        choices:
        - RECEIVE
        - SEND
    partner:
        description: Partner of the transfer
        type: str
    idf:
        description: Flow identifier.
        type: str
    api_timeout:
        description: Command timeout.
        type: int
    filename:
        description: File to be sent.
        type: str
    parm:
        description: Additional information about the transfer.
        type: str
    idm:
        description: Message identifier.
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
        - nacknowledged
        - ended
'''

EXAMPLES = r'''
- name: Send a new transfer message
  axway_cft_transfer:
    partner: PARIS
    ida: my_custom_id
    idm: MESSAGEID
    msg: My little message

- name: Create a new send file transfer request
  axway_cft_transfer:
    direction: SEND
    partner: PARIS
    idf: SMSU001
    filename: C:/tmp/my_file.txt

- name: Create a new receive file transfer request
  axway_cft_transfer:
    direction: RECEIVE
    partner: NEWYORK
    idf: SMSU002
    filename: C:/tmp/my_incoming_file.txt

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
    elements: dict
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
        links: string
        rel: string
        href: string
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_cft_transfers import (
    delete_transfer, create_message_transfer_request, create_send_file_transfer_request, create_receive_file_transfer_request, fetch_transfer, fetch_transfers,
    halt_transfer, keep_transfer, start_transfer, submit_transfer, resume_transfer, ack_transfer, nack_transfer, end_transfer
)

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

from ansible_collections.warkdev.axway_cft.plugins.module_utils.common import AxwayModuleError

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            idtu=dict(type='str'),
            state=dict(type='str', default='present',
                       choices=['present', 'absent', 'halted', 'kept', 'started', 'resumed', 'submitted', 'acknowledged', 'nacknowledged', 'ended']),
            direction=dict(type='str', choices=['SEND', 'RECEIVE']),
            partner=dict(type='str'),
            idf=dict(type='str'),
            api_timeout=dict(type='int'),
            filename=dict(type='str'),
            parm=dict(type='str'),
            idm=dict(type='str'),
            msg=dict(type='str'),
            ida=dict(type='str')
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_if = [
            ['state', 'present', ['direction', 'partner', 'idf', 'filename', 'idm', 'msg'], True],
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
            ['direction', 'idm'],
            ['direction', 'msg'],
            ['idf', 'idm'],
            ['idf', 'msg'],
            ['filename', 'idm'],
            ['filename', 'msg']
        ]
        self.required_by = {
            'direction': ['partner', 'idf', 'filename'],
            'idm': ['msg']
        }


def __exec_post(module, **kwargs):
    cft_data = {}
    if 'ida' in kwargs and kwargs['ida']:
        cft_data = fetch_transfers(module, ida=kwargs['ida'])['transfers'][0]
    if cft_data:  # Some transfer data already exist, no need to re-create
        response = {'changed': False, 'transfer': cft_data}
    elif 'msg' in kwargs and kwargs['msg']:
        # User trying to create a new message transfer
        if module.check_mode:
            response = {'changed': True, 'transfer': {}}  # Change state is reported only if CFT Data doesn't exists
        else:
            response = create_message_transfer_request(module, partner=kwargs['partner'], idm=kwargs['idm'], msg=kwargs['msg'],
                                                       apitimeout=kwargs.get('api_timeout'), ida=kwargs.get('ida'))
    elif 'filename' in kwargs and kwargs['filename']:
        if module.check_mode:
            response = {'changed': True, 'transfer': {}}
        # User trying to create a new file transfer
        elif kwargs['direction'] == 'SEND':
            response = create_send_file_transfer_request(module, partner=kwargs['partner'], idf=kwargs['idf'], apitimeout=kwargs.get('api_timeout'),
                                                         ida=kwargs.get('ida'), fname=kwargs['filename'], parm=kwargs.get('parm'))
        elif kwargs['direction'] == 'RECEIVE':
            response = create_receive_file_transfer_request(module, partner=kwargs['partner'], idf=kwargs['idf'], apitimeout=kwargs.get('api_timeout'),
                                                            ida=kwargs.get('ida'), fname=kwargs['filename'], parm=kwargs.get('parm'))

    return response


def __exec_delete(module, **kwargs):
    try:
        cft_data = fetch_transfer(module, idtu=kwargs['idtu'])
    except AxwayModuleError:
        cft_data = {}
    if cft_data:
        response = delete_transfer(module, idtu=kwargs['idtu'])
    else:  # There's no matching transfer
        response = {'changed': False, 'transfer': cft_data}
    return response


def __exec_halt(module, **kwargs):
    response = halt_transfer(module, idtu=kwargs['idtu'])
    return response


def __exec_keep(module, **kwargs):
    response = keep_transfer(module, idtu=kwargs['idtu'])
    return response


def __exec_start(module, **kwargs):
    response = start_transfer(module, idtu=kwargs['idtu'])
    return response


def __exec_resume(module, **kwargs):
    response = resume_transfer(module, idtu=kwargs['idtu'])
    return response


def __exec_submit(module, **kwargs):
    response = submit_transfer(module, idtu=kwargs['idtu'])
    return response


def __exec_ack(module, **kwargs):
    response = ack_transfer(module, idtu=kwargs['idtu'], idm=kwargs['idm'], msg=kwargs['msg'])
    return response


def __exec_nack(module, **kwargs):
    response = nack_transfer(module, idtu=kwargs['idtu'], idm=kwargs['idm'], msg=kwargs['msg'])
    return response


def __exec_end(module, **kwargs):
    response = end_transfer(module, idtu=kwargs['idtu'])
    return response


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

    return response


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
