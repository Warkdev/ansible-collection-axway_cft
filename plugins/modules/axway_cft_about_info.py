#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_about_info
short_description: Get the version of Axway Transfer CFT
description:
  - Get the version of Axway Transfer CFT.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options: {}
extends_documentation_fragment:
  - community.axway_cft.logging_info_options
'''

EXAMPLES = r'''
- name: Collect Axway Transfer CFT version
  axway_cft_about_info:
'''

RETURN = r'''
about_info:
  description: Dictionnary about Axway Transfer CFT Server
  returned: always
  type: dict
  contains:
    cft_version:
      description: The version of the CFT
      returned: always
      type: str
      sample: "3.3.2"
    cft_level:
      description: The level of CFT, SP and patch
      returned: always
      type: str
      sample: ""
    cft_system:
      description: System running CFT
      returned: always
      type: str
      sample: "unix"
    cft_server_time:
      description: Local time on CFT server
      returned: always
      type: str
      sample: "1526301034000"
    cft_server_utc:
      description: UTC Timezone on CFT server
      returned: always
      type: str
      sample: "2"
    multinode_enabled:
      description: CFT is in mutinode mode
      returned: always
      type: bool
      sample: True
    cft_cg_enabled:
      description: CFT is controlled by Control Governance
      returned: always
      type: bool
      sample: False
    cft_instance_id:
      description: The instance ID of CFT
      returned: always
      type: str
      sample: "workstationaddress"
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.axway_cft.plugins.module_utils.axway_cft_about import fetch_about

from ansible_collections.community.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

from ansible_collections.community.axway_cft.plugins.module_utils.common import (
    flattened_to_bool
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict()
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_get_facts(module):
    response = fetch_about(module=module)
    return response


def exec_module(module):
    response = __exec_get_facts(module=module)
    about_info = {
        'version': response['version'],
        'level': response['level'],
        'system': response['system'],
        'server_time': response['server_time'],
        'server_utc': response['server_utc'],
        'multinode_enabled': bool(flattened_to_bool(response['multinode_enabled'])),
        'cg_enabled': bool(flattened_to_bool(response['cg_enabled'])),
        'instance_id': response['instance_id']
    }
    return {'changed': False, 'about_info': about_info}


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
