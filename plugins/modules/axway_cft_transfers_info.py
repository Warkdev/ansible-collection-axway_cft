#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_transfers_info
short_description: Retrieves content about several transfers at once.
description:
  - Retrieve current transfers.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    ida:
        description: Transfer-related identifier.
        type: str
    idtu:
        description: Transfer ID.
        type: str
    idt:
        description: Protocol transfer ID.
        type: str
    nidt:
        description: Network protocol transfer ID.
        type: str
    part:
        description: Partner associated with the transfer.
        type: str
    idf:
        description: Flow ID.
        type: str
    phase:
        description: Transfer phase.
        type: str
        choices: ['A', 'T', 'Y', 'Z', 'X']
    phasestep:
        description: Transfer phasestep.
        type: str
        choices: ['D', 'C', 'E', 'K', 'H', 'X']
    fields:
        description: List of fields to return.
        type: list
        elements: str
        default:
        - PART
        - DIRECT
        - TYPE
        - COMPATSTATE
        - ACK
        - STATE
        - PHASE
        - PHASESTEP
        - IDF
        - IDT
        - IDTU
        - PIDTU
        - NREC
        - FREC
        - MSG
        - DIAGI
        - DIAGP
        - REQUSER
        - REQGROUP
        - IDA
    offset:
        description: Catalog offset.
        type: int
        default: 0
    limit:
        description: Maximum number of transfers to return.
        type: int
        default: 100
'''

EXAMPLES = r'''
- name: Gather all transfers
  axway_cft_transfers_info:
  register: transfers

- name: Gather transfers in the phase 'X'
  axway_cft_transfers_info:
    phase: X
  register: transfers

- name: Gather transfers with PARIS
  axway_cft_transfers_info:
    part: PARIS
  register: transfers

- name: Gather transfers and limit the amount of fields returned
  axway_cft_transfers_info:
    fields:
    - PART
    - DIRECT
    - STATE
    - PHASE
  register: transfers
'''

RETURN = r'''
transfers:
    description: A list of transfers corresponding to the matching criteria's
    returned: always
    type: list
    elements: dict
    sample:
        - partner: "PARIS"
          direct: "INCOMING"
          type: "string"
          compatstate: "string"
          ack: "string"
          state: "string"
          phase: "string"
          phasestep: "string"
          idf: "string"
          idt: "string"
          idtu: "string"
          pidtu: "string"
          nrec: "string"
          frec: "string"
          msg: "string"
          diagi: "string
          diagp: "string"
          requser: "string"
          reqgroup: "string"
          ida: "string"
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_cft_transfers import fetch_transfers

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
            ida=dict(type='str'),
            idtu=dict(type='str'),
            idt=dict(type='str'),
            nidt=dict(type='str'),
            part=dict(type='str'),
            idf=dict(type='str'),
            phase=dict(type='str', choices=['A', 'T', 'Y', 'Z', 'X']),
            phasestep=dict(type='str', choices=['D', 'C', 'E', 'K', 'H', 'X']),
            fields=dict(type='list', elements='str', default=['PART', 'DIRECT', 'TYPE', 'COMPATSTATE', 'ACK', 'STATE', 'PHASE', 'PHASESTEP' , 'IDF', 'IDT', 'IDTU', 'PIDTU', 'NREC', 'FREC', 'MSG', 'DIAGI', 'DIAGP', 'REQUSER', 'REQGROUP', 'IDA']),
            offset=dict(type='int', default=0),
            limit=dict(type='int', default=100)
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_get(module, **kwargs):
    response = fetch_transfers(module=module, **kwargs)
    return response


def exec_module(module):
    response = __exec_get(module=module, **module.params)
    return {'transfers': response['transfers']}


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
